"""Focused, in-memory extraction contracts. Never runs the full extractor."""
import contextlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sqlite3
import unittest
from unittest import mock

import ifcopenshell
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rich_extractor",
    ROOT / "DAGCompiler/python/extractIFCtoDB.py")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


def box(lo, hi):
    v = np.array([[0,0,lo],[2,0,lo],[2,3,lo],[0,3,lo],
                  [0,0,hi],[2,0,hi],[2,3,hi],[0,3,hi]], dtype=float)
    f = np.array([[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],
                  [1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]], dtype=np.int32)
    return v, f


class Layers(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        cm = contextlib.redirect_stdout(self.output)
        cm.__enter__()
        self.addCleanup(cm.__exit__, None, None, None)

    def db(self, ts, *, sense="POSITIVE", offset=0.0, frame=None, span=None):
        c = sqlite3.connect(":memory:")
        self.addCleanup(c.close)
        c.executescript(E.REFERENCE_SCHEMA)
        frame = np.eye(4) if frame is None else frame
        total = sum(t for t in ts if t is not None and math.isfinite(t))
        size = total if total > 0 else 1.0
        lo, hi = span or ((offset, offset+size) if sense == "POSITIVE"
                         else (offset-size, offset))
        v, f = box(lo, hi)
        v = (v @ frame[:3,:3].T + frame[:3,3]).astype(np.float32)
        c.execute("INSERT INTO base_geometries VALUES (?,?,?,?,?)",
                  ("host",v.tobytes(),f.tobytes(),len(v),len(f)))
        c.execute("INSERT INTO element_instances VALUES ('element','host')")
        c.execute("INSERT INTO rel_material_layer_set VALUES (?,?,?,?,?,?,?,?)",
                  ("element","set",len(ts),total,"AXIS3",sense,offset,"ifc:IfcMaterialLayerSetUsage"))
        c.execute("INSERT INTO material_layer_frames VALUES (?,?,?)",
                  ("element",json.dumps(frame.tolist()),"ifc:test-authored-frame"))
        c.executemany("INSERT INTO material_layers VALUES (?,?,?,?,?)",
                      [("set",i,"material-"+str(i),t,0) for i,t in enumerate(ts)])
        c.commit()
        return c

    def compile_ok(self,c):
        count, refused, _ = E.compile_layer_geometry(c)
        self.assertFalse(refused, self.output.getvalue())
        self.assertGreater(count,0)
        self.assertEqual(E.verify_layer_geometry(c),0,self.output.getvalue())
        return c

    def seqs(self,c):
        return [r[0] for r in c.execute(
            "SELECT layer_seq FROM component_geometry_layers ORDER BY layer_seq")]

    def rejects(self,ts):
        c=self.db(ts)
        self.assertTrue(E.compile_layer_geometry(c)[1])
        self.assertGreater(E.verify_layer_geometry(c),0)
        self.assertEqual(c.execute("SELECT COUNT(*) FROM component_geometry_layers").fetchone()[0],0)

    def test_one_positive(self):
        self.assertEqual(self.seqs(self.compile_ok(self.db([1.0]))),[0])

    def test_zero_between_positive(self):
        self.assertEqual(self.seqs(self.compile_ok(self.db([.3,0,.7]))),[0,2])

    def test_multiple_zero(self):
        self.assertEqual(self.seqs(self.compile_ok(self.db([.3,0,0,.7]))),[0,3])

    def test_leading_zero(self):
        self.assertEqual(self.seqs(self.compile_ok(self.db([0,.3,.7]))),[1,2])

    def test_trailing_zero(self):
        self.assertEqual(self.seqs(self.compile_ok(self.db([.3,.7,0]))),[0,1])

    def test_all_zero(self):
        self.rejects([0,0])

    def test_negative(self):
        self.rejects([-.1,1.1])

    def test_missing(self):
        self.rejects([None,1])

    def test_nonfinite(self):
        for t in [float("inf"),float("-inf"),float("nan")]:
            with self.subTest(t=t): self.rejects([t,1])

    def test_semantics_and_no_invented_thickness(self):
        c=self.db([.3,0,0,.7])
        before=c.execute("SELECT * FROM material_layers ORDER BY sequence").fetchall()
        self.compile_ok(c)
        self.assertEqual(c.execute("SELECT * FROM material_layers ORDER BY sequence").fetchall(),before)
        self.assertEqual(c.execute("SELECT SUM(thickness_m) FROM component_geometry_layers").fetchone()[0],1)
        self.assertEqual(c.execute("SELECT COUNT(*) FROM component_geometry_layers WHERE face_count<=0").fetchone()[0],0)

    def test_deterministic_order(self):
        a=self.db([.3,0,.7]);b=self.db([.3,0,.7])
        rows=b.execute("SELECT * FROM material_layers").fetchall()
        b.execute("DELETE FROM material_layers")
        b.executemany("INSERT INTO material_layers VALUES (?,?,?,?,?)",reversed(rows))
        self.compile_ok(a);self.compile_ok(b)
        for table in ["component_geometry_layers","base_geometries"]:
            self.assertEqual(a.execute("SELECT * FROM "+table).fetchall(),
                             b.execute("SELECT * FROM "+table).fetchall())

    def test_envelope_conservation(self):
        c=self.compile_ok(self.db([.3,0,.7]))
        v,f=c.execute("SELECT vertices,faces FROM base_geometries").fetchone()
        v=np.frombuffer(v,np.float32).reshape(-1,3)
        f=np.frombuffer(f,np.int32).reshape(-1,3)
        self.assertAlmostEqual(E._mesh_signed_volume(v,f),6.0,places=5)
        np.testing.assert_allclose(v.min(0),[0,0,0])
        np.testing.assert_allclose(v.max(0),[2,3,1])

    def test_invalid_host(self):
        c=self.db([.3,.7])
        f=c.execute("SELECT faces FROM base_geometries").fetchone()[0]
        c.execute("UPDATE base_geometries SET faces=?,face_count=11",(f[:-12],))
        self.assertTrue(E.compile_layer_geometry(c)[1])

    def layer_bounds(self,c,seq):
        v,f=c.execute("SELECT vertices,faces FROM base_geometries LIMIT 1").fetchone()
        v=np.frombuffer(v,np.float32).reshape(-1,3)
        f=np.frombuffer(f,np.int32).reshape(-1,3)
        fs,fc=c.execute("SELECT face_start,face_count FROM component_geometry_layers WHERE layer_seq=?",(seq,)).fetchone()
        used=v[np.unique(f[fs:fs+fc])]
        return used.min(0),used.max(0)

    def test_downward_frame_order(self):
        frame=np.diag([1.,-1.,-1.,1.])
        c=self.compile_ok(self.db([.3,0,.7],frame=frame))
        lo,hi=self.layer_bounds(c,0)
        self.assertAlmostEqual(float(lo[2]),-.3,places=6)
        self.assertAlmostEqual(float(hi[2]),0,places=6)

    def test_rotated_frame(self):
        frame=np.array([[0,0,1,4],[0,1,0,5],[-1,0,0,6],[0,0,0,1]],dtype=float)
        c=self.compile_ok(self.db([.3,0,.7],frame=frame))
        lo,hi=self.layer_bounds(c,0)
        self.assertAlmostEqual(float(lo[0]),4,places=5)
        self.assertAlmostEqual(float(hi[0]),4.3,places=5)

    def test_negative_sense(self):
        c=self.compile_ok(self.db([.3,0,.7],sense="NEGATIVE",offset=1))
        lo,hi=self.layer_bounds(c,0)
        self.assertAlmostEqual(float(lo[2]),.7,places=6)
        self.assertAlmostEqual(float(hi[2]),1,places=6)

    def test_nonzero_offset(self):
        c=self.compile_ok(self.db([.3,.7],offset=2.0))
        lo,hi=self.layer_bounds(c,0)
        self.assertAlmostEqual(float(lo[2]),2,places=5)
        self.assertAlmostEqual(float(hi[2]),2.3,places=5)

    def test_missing_positive_geometry(self):
        c=self.compile_ok(self.db([.3,0,.7]))
        c.execute("DELETE FROM component_geometry_layers WHERE layer_seq=2")
        self.assertGreater(E.verify_layer_geometry(c),0)

    def test_empty_index_row(self):
        c=self.compile_ok(self.db([.3,.7]))
        c.execute("UPDATE component_geometry_layers SET face_count=0 WHERE layer_seq=0")
        self.assertGreater(E.verify_layer_geometry(c),0)

    def test_missing_verification_tables(self):
        for table in ["material_layers","material_layer_frames","layer_geometry_source",
                      "component_geometry_layers","rel_material_layer_set","element_instances","base_geometries"]:
            with self.subTest(table=table):
                c=self.compile_ok(self.db([.3,.7]))
                c.execute("DROP TABLE "+table)
                self.assertGreater(E.verify_layer_geometry(c),0)

    def test_clipped_whole_layer(self):
        c=self.compile_ok(self.db([.2,.3,.5],span=(0,.5)))
        self.assertEqual(self.seqs(c),[0,1])

    def test_partial_layer_clip_rejected(self):
        c=self.db([.2,.3,.5],span=(0,.6))
        self.assertTrue(E.compile_layer_geometry(c)[1])

    def test_shared_mesh_different_usage(self):
        c=self.db([.3,0,.7])
        c.execute("INSERT INTO element_instances VALUES ('other','host')")
        c.execute("INSERT INTO rel_material_layer_set SELECT 'other','other-set',3,1,'AXIS3','NEGATIVE',1,provenance FROM rel_material_layer_set")
        c.execute("INSERT INTO material_layer_frames SELECT 'other',frame_json,provenance FROM material_layer_frames")
        c.executemany("INSERT INTO material_layers VALUES ('other-set',?,?,?,0)",
                      [(0,"different",.4),(1,"membrane",0),(2,"other",.6)])
        self.compile_ok(c)
        hashes=dict(c.execute("SELECT guid,geometry_hash FROM element_instances"))
        self.assertNotEqual(hashes["element"],hashes["other"])
        rows=c.execute("SELECT layer_seq,material_name FROM component_geometry_layers WHERE geometry_hash=? ORDER BY layer_seq",(hashes["other"],)).fetchall()
        self.assertEqual(rows,[(0,"different"),(2,"other")])

    def test_deleted_semantic_zero_fails(self):
        c=self.compile_ok(self.db([.3,0,.7]))
        c.execute("DELETE FROM material_layers WHERE sequence=1")
        self.assertGreater(E.verify_layer_geometry(c),0)

    def test_wrong_material_order_fails(self):
        c=self.compile_ok(self.db([.3,.7]))
        c.execute("UPDATE component_geometry_layers SET material_name='wrong' WHERE layer_seq=0")
        self.assertGreater(E.verify_layer_geometry(c),0)

    def test_geometry_shift_gap_fails(self):
        c=self.compile_ok(self.db([.3,.7]))
        blob=c.execute("SELECT vertices FROM base_geometries").fetchone()[0]
        v=np.frombuffer(blob,np.float32).copy().reshape(-1,3);v[:,0]+=.1
        c.execute("UPDATE base_geometries SET vertices=?",(v.tobytes(),))
        self.assertGreater(E.verify_layer_geometry(c),0)

    def test_no_bbox_reanchoring(self):
        c=self.db([.3,.7],span=(2,3))
        self.assertTrue(E.compile_layer_geometry(c)[1])

    def test_missing_frame_refused(self):
        c=self.db([.3,.7])
        c.execute("DELETE FROM material_layer_frames")
        self.assertTrue(E.compile_layer_geometry(c)[1])

    def test_type_definition_not_an_unmeshed_occurrence(self):
        c=self.compile_ok(self.db([.3,.7]))
        c.execute("INSERT INTO rel_material_layer_set VALUES ('type','set',2,1,NULL,NULL,NULL,'ifc:IfcMaterialLayerSet')")
        c.execute("INSERT INTO material_layer_frames VALUES ('type','null','ifc:type-definition')")
        self.assertEqual(E.verify_layer_geometry(c),0)
        c.execute("UPDATE material_layer_frames SET provenance='unresolved:missing' WHERE element_guid='type'")
        self.assertGreater(E.verify_layer_geometry(c),0)

    def test_missing_occurrence_fails(self):
        c=self.compile_ok(self.db([.3,.7]))
        c.execute("DELETE FROM element_instances")
        self.assertGreater(E.verify_layer_geometry(c),0)

    def test_geometry_overlap_fails(self):
        c=self.compile_ok(self.db([.5,.5]))
        v,f=c.execute("SELECT vertices,faces FROM base_geometries").fetchone()
        v=np.frombuffer(v,np.float32).copy().reshape(-1,3)
        f=np.frombuffer(f,np.int32).reshape(-1,3)
        fs,fc=c.execute("SELECT face_start,face_count FROM component_geometry_layers WHERE layer_seq=1").fetchone()
        v[np.unique(f[fs:fs+fc]),2]-=.1
        c.execute("UPDATE base_geometries SET vertices=?",(v.tobytes(),))
        self.assertGreater(E.verify_layer_geometry(c),0)

    def test_idempotent_compile_reverifies_source(self):
        c=self.compile_ok(self.db([.3,0,.7]))
        blobs=c.execute("SELECT * FROM base_geometries").fetchall()
        self.assertEqual(E.compile_layer_geometry(c)[0],0)
        self.assertEqual(E.verify_layer_geometry(c),0)
        self.assertEqual(c.execute("SELECT * FROM base_geometries").fetchall(),blobs)
        c.execute("UPDATE material_layers SET thickness_m=.001 WHERE sequence=1")
        self.assertGreater(E.verify_layer_geometry(c),0)



class Node:
    next_id=0
    def __init__(self,kind,name=None):
        Node.next_id+=1; self.number=Node.next_id
        self.kind=kind; self.Name=name; self.GlobalId=str(self.number)
        self.ContainedInStructure=[];self.Decomposes=[];self.Nests=[];self.VoidsElements=[]
    def id(self): return self.number
    def is_a(self,kind): return self.kind==kind


def link(child,attr,parent,field):
    rel=type("Relation",(),{})()
    setattr(rel,field,parent);getattr(child,attr).append(rel)


def contain(child,parent): link(child,"ContainedInStructure",parent,"RelatingStructure")
def aggregate(child,parent): link(child,"Decomposes",parent,"RelatingObject")


class Storeys(unittest.TestCase):
    def setUp(self):
        self.floor=Node("IfcBuildingStorey","Level A");self.element=Node("IfcMember")
    def test_direct(self):
        contain(self.element,self.floor)
        self.assertEqual(E.get_storey_for_element(self.element),"Level A")
    def test_space(self):
        space=Node("IfcSpace");aggregate(space,self.floor);contain(self.element,space)
        self.assertEqual(E.get_storey_for_element(self.element),"Level A")
    def test_aggregate(self):
        parent=Node("IfcCurtainWall");aggregate(self.element,parent);contain(parent,self.floor)
        self.assertEqual(E.get_storey_for_element(self.element),"Level A")
    def test_multilevel(self):
        a=Node("IfcElementAssembly");b=Node("IfcCurtainWall")
        aggregate(self.element,a);aggregate(a,b);contain(b,self.floor)
        self.assertEqual(E.get_storey_for_element(self.element),"Level A")
    def test_opening_host(self):
        opening=Node("IfcOpeningElement");contain(self.element,self.floor)
        link(opening,"VoidsElements",self.element,"RelatingBuildingElement")
        self.assertEqual(E.get_storey_for_element(opening),"Level A")
    def test_duplicate_paths(self):
        contain(self.element,self.floor);aggregate(self.element,self.floor)
        self.assertEqual(E.get_storey_for_element(self.element),"Level A")
    def test_conflict(self):
        contain(self.element,self.floor)
        aggregate(self.element,Node("IfcBuildingStorey","Level B"))
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(E.get_storey_for_element(self.element),"Unknown")
        self.assertIn("conflicting storeys",out.getvalue())
    def test_cycle(self):
        other=Node("IfcMember");aggregate(self.element,other);aggregate(other,self.element)
        self.assertEqual(E.get_storey_for_element(self.element),"Unknown")
        contain(other,self.floor)
        self.assertEqual(E.get_storey_for_element(self.element),"Level A")
    def test_uncontained(self):
        self.assertEqual(E.get_storey_for_element(self.element),"Unknown")
    def test_crossing_elevation(self):
        self.element.min_z=-100;self.element.max_z=100;self.floor.Elevation=0
        contain(self.element,self.floor)
        self.assertEqual(E.get_storey_for_element(self.element),"Level A")
    def test_samplehouse_relationships_only(self):
        model=ifcopenshell.open(str(ROOT/"reference/residential/Ifc4_SampleHouse.ifc"))
        for cls,count in [("IfcMember",20),("IfcPlate",6),("IfcOpeningElement",7)]:
            elems=model.by_type(cls)
            self.assertEqual(len(elems),count)
            self.assertTrue(all(E.get_storey_for_element(e)=="Ground Floor" for e in elems))


class SourceFrames(unittest.TestCase):
    def synthetic_slab(self):
        m=ifcopenshell.file(schema="IFC4")
        point=m.create_entity("IfcCartesianPoint",(1000.,2000.,3000.))
        axis=m.create_entity("IfcDirection",(1.,0.,0.))
        ref=m.create_entity("IfcDirection",(0.,1.,0.))
        position=m.create_entity("IfcAxis2Placement3D",point,axis,ref)
        direction=m.create_entity("IfcDirection",(0.,0.,1.))
        profile=m.create_entity("IfcRectangleProfileDef",ProfileType="AREA",XDim=2000.,YDim=3000.)
        item=m.create_entity("IfcExtrudedAreaSolid",profile,position,direction,1000.)
        rep=m.create_entity("IfcShapeRepresentation",RepresentationIdentifier="Body",
                            RepresentationType="SweptSolid",Items=[item])
        shape=m.create_entity("IfcProductDefinitionShape",Representations=[rep])
        slab=m.create_entity("IfcSlab",GlobalId=ifcopenshell.guid.new(),Representation=shape)
        return m,slab,item

    def test_rotated_authored_frame_and_element_transform(self):
        m,slab,item=self.synthetic_slab()
        frame,source=E.material_layer_frame(slab,"AXIS3",.001)
        frame=np.array(frame)
        np.testing.assert_allclose(frame[:3,2],[1,0,0])
        np.testing.assert_allclose(frame[:3,3],[1,2,3])
        # Element placement is applied later by the instance transform, not twice.
        point=m.create_entity("IfcCartesianPoint",(9000.,8000.,7000.))
        axis=m.create_entity("IfcDirection",(0.,0.,1.))
        ref=m.create_entity("IfcDirection",(0.,1.,0.))
        pos=m.create_entity("IfcAxis2Placement3D",point,axis,ref)
        slab.ObjectPlacement=m.create_entity("IfcLocalPlacement",RelativePlacement=pos)
        again,_=E.material_layer_frame(slab,"AXIS3",.001)
        np.testing.assert_allclose(again,frame)
        world=E._placement_matrix(slab);world[:3,3]*=.001
        # Source +Z is local +X, then world +Y after element rotation.
        np.testing.assert_allclose(world[:3,:3] @ frame[:3,2],[0,1,0])

    def test_ambiguous_body_refuses(self):
        m,slab,item=self.synthetic_slab()
        slab.Representation.Representations[0].Items=[item,item]
        frame,source=E.material_layer_frame(slab,"AXIS3",.001)
        self.assertIsNone(frame)
        self.assertEqual(source,"unresolved:ambiguous-body-items")

    def test_nonperpendicular_extrusion_refuses(self):
        m,slab,item=self.synthetic_slab()
        item.ExtrudedDirection=m.create_entity("IfcDirection",(1.,0.,1.))
        self.assertIsNone(E.material_layer_frame(slab,"AXIS3",.001)[0])

    def test_samplehouse_swept_frame_without_tessellation(self):
        model=ifcopenshell.open(str(ROOT/"reference/residential/Ifc4_SampleHouse.ifc"))
        slab=next(e for e in model.by_type("IfcSlab")
                  if any(r.is_a("IfcRelAssociatesMaterial") and
                         r.RelatingMaterial.is_a("IfcMaterialLayerSetUsage") and
                         len(r.RelatingMaterial.ForLayerSet.MaterialLayers)==7
                         for r in e.HasAssociations))
        frame,source=E.material_layer_frame(slab,"AXIS3",.001)
        np.testing.assert_allclose(np.asarray(frame)[:3,2],[0,0,-1])
        self.assertTrue(source.startswith("ifc:"))
        rows=E.extract_rel_material_layer_set(model)
        row=next(r for r in rows if r["element_guid"]==slab.GlobalId)
        self.assertEqual(row["direction_sense"],"POSITIVE")
        self.assertEqual(row["offset_from_reference_line"],0)
        np.testing.assert_allclose(row["frame"],frame)
        c=sqlite3.connect(":memory:")
        self.addCleanup(c.close)
        c.executescript(E.REFERENCE_SCHEMA)
        E.write_material_layers(c,E.extract_material_layers(model))
        E.write_rel_material_layer_set(c,rows)
        saved=c.execute("SELECT frame_json,provenance FROM material_layer_frames WHERE element_guid=?",(slab.GlobalId,)).fetchone()
        self.assertIsNotNone(saved)
        np.testing.assert_allclose(json.loads(saved[0]),frame)
        self.assertTrue(saved[1].startswith("ifc:"))
        for r in rows:
            self.assertEqual(c.execute(
                "SELECT provenance FROM rel_material_layer_set WHERE element_guid=?",
                (r["element_guid"],)).fetchone()[0],r["provenance"])


class ProofExit(unittest.TestCase):
    def test_failed_proof_remains_fatal(self):
        def failed(*args,**kwargs): E.LAST_PROOF_FAIL=1
        with mock.patch.object(E,"extract_reference",failed), mock.patch.object(
                E.sys,"argv",["extract","--ifc","not-opened","-o","not-created"]):
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as cm:
                E.main()
        self.assertEqual(cm.exception.code,1)
        E.LAST_PROOF_FAIL=0

    def test_successful_mock_proof_exit(self):
        with mock.patch.object(E,"extract_reference"), mock.patch.object(
                E.sys,"argv",["extract","--ifc","not-opened","-o","not-created"]):
            E.LAST_PROOF_FAIL=0
            E.main()


if __name__=="__main__":
    unittest.main(verbosity=2)
