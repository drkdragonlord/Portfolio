//
// Copyright (C) Juan Borrero
// 
// File: pluginMain.h
//
// Author: Maya Plug-in Wizard 2.0
//

#ifdef WIN32
	#pragma once
	// this is needed before any of the maya includes. Generally it is better to
	// set this within the preprocessor settings of visual C++.
	//#define NT_PLUGIN
#endif

#ifdef WIN32
	#include <windows.h>
#endif

#include <math.h>
#include <string.h>
#include <vector>
#include <assert.h>
#include <maya/MIOStream.h>

#include <maya/MNodeMessage.h>
#include <maya/MDGMessage.h>
#include <maya/MTypeId.h>
#include <maya/MGlobal.h>
#include <maya/MLibrary.h>
#include <maya/MPxLocatorNode.h>
#include <maya/MPxTransform.h>
#include <maya/MPxDeformerNode.h> 
#include <maya/MPxCommand.h>
#include <maya/MPxNode.h>
#include <maya/MPxSurfaceShape.h>
#include <maya/MPxSurfaceShapeUI.h>
#include <maya/MPxGeometryData.h>
#include <maya/MPxGeometryIterator.h>
#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>
#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MArgList.h>
#include <maya/MFnPluginData.h>

#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsSurface.h>
#include <maya/MFnMesh.h>
#include <maya/MFnSubd.h>
#include <maya/MFnNurbsSurfaceData.h>
#include <maya/MFnNurbsCurveData.h>

#include <maya/MManipData.h>
#include <maya/MPxManipContainer.h> 
#include <maya/MFnDistanceManip.h> 
#include <maya/MFnCircleSweepManip.h>
#include <maya/MFnFreePointTriadManip.h>
#include <maya/MFnStateManip.h>
#include <maya/MFnToggleManip.h>
#include <maya/MPxContext.h>
#include <maya/MPxSelectionContext.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnGenericAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MAttributeIndex.h>
#include <maya/MAttributeSpec.h>
#include <maya/MAttributeSpecArray.h>

#include <maya/MDGModifier.h>
#include <maya/MDagModifier.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnDagNode.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MFnTransform.h>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MDagModifier.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MObjectArray.h>

#include <maya/MString.h>
#include <maya/MStringArray.h>
#include <maya/MFnStringData.h>
#include <maya/MFnStringArrayData.h>
#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MVector.h>
#include <maya/MVectorArray.h>
#include <maya/MFnVectorArrayData.h>
#include <maya/MIntArray.h>
#include <maya/MDistance.h>
#include <maya/MAngle.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFloatMatrix.h>
#include <maya/MFloatPointArray.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MQuaternion.h>
#include <maya/MEulerRotation.h>
#include <maya/MFnIkJoint.h>

#include <maya/MColor.h>
#include <maya/MColorArray.h>
#include <maya/M3dView.h>
#include <maya/MDrawData.h>
#include <maya/MDrawRequest.h>
#include <maya/MMaterial.h>
#include <maya/MImage.h>
#include <maya/MRenderUtil.h>
#include <maya/MTime.h>
#include <maya/MAnimControl.h>

#include <maya/MItGeometry.h>
#include <maya/MSelectionList.h>
#include <maya/MItSelectionList.h>
#include <maya/MSelectionMask.h>
#include <maya/MItDependencyGraph.h>
#include <maya/MFnGeometryFilter.h>
#include <maya/MFnSet.h>
#include <maya/MFnMeshData.h>
#include <maya/MItMeshEdge.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MItMeshVertex.h>
#include <maya/MItMeshFaceVertex.h>