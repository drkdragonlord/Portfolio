//

#ifndef __LOCATOR_H__
#define __LOCATOR_H__

	#ifdef WIN32
		#pragma once
		// this is needed before any of the maya includes. Generally it is better to
		// set this within the preprocessor settings of visual C++.
		#define NT_PLUGIN
	#endif

	#include <maya/MPxLocatorNode.h>
	#include <maya/MString.h>
	#include <maya/MTypeId.h>
	#include <maya/MVector.h>
	#include <maya/MDataBlock.h>
	#include <maya/MDataHandle.h>
	#include <maya/M3dView.h>
	#include <maya/MDistance.h>
	#include <maya/MFnUnitAttribute.h>
	#include <maya/MFnNumericAttribute.h>
	#include <maya/MFnMessageAttribute.h>
	#include <maya/MFnTypedAttribute.h>
	#include <maya/MPxManipContainer.h>
	#include <maya/MPointArray.h>
	#include <math.h>
	#include <maya/MStreamUtils.h>
	#include <maya/MIOStream.h>

	/// This class defines our new locator node type we will add into maya. We simply
	/// need to derive our class from MPxLocatorNode, and overload a number of specific
	/// functions.
	///
	/// We require the following functions for our locator :
	///
	/// 	* a couple of functions to create and initialise our locator node.
	///
	/// 	* for selection purposes, we need to define a bounding box for our
	/// 	  locator node. Maya then uses this information to determine whether
	/// 	  the user selected this node.
	///
	/// 	* a draw function. This is the fun bit, we need to make the appropriate
	/// 	  openGL calls to render our locator node. We can use as much artistic
	/// 	  license as we want here, though it's generally sensible to use
	/// 	  colours that reflect the user settings in some way.
	///
	///	The final thing that all custom nodes require is some type information to
	/// help maya identify the node type. We need a typename so that mel scripts
	/// can identify the nodes type. In addition all custom nodes must provide a
	/// typeID.
	///
	/// Simply put, when maya saves or loads a scene, it needs to be able read
	/// and write the node to a file. It therefore needs a quick method of identifying
	/// the node data in the file. An integer is quicker and easier to use for this
	/// purpose than the type name as a string.
	///
	class jbMuscleCage : public MPxLocatorNode
	{
	public:

		/// \brief	This function is used to render our custom locator node
		/// \param	view	-	the maya viewport to render the locator node in
		/// \param	DGpath	-	the DAG path of the object
		/// \param	style	-	wireframe, shaded etc
		/// \param	status	-	normal, selected, templated etc
		///
		virtual void draw( M3dView&, const MDagPath&, M3dView::DisplayStyle, M3dView::DisplayStatus);

		/// \brief	this function can tell maya whether the locator node has a volume
		/// \return	true if bounded, false otherwise.
		///
		virtual bool isBounded() const;

		/// \brief	returns the bounding box of the locator node
		/// \return	the nodes bounding box
		virtual MBoundingBox boundingBox() const;

		/// \brief	this function is called by mata to return a new instance of our locator node
		/// \return	the new node
		static void* creator();

		/// \brief	this function creates a description of our node
		/// \return	The status code
		static MStatus initialize();

	// type information
	public:

		/// the unique type ID of our custom node. Used internally by maya for fileIO.
		static const MTypeId typeId;

		/// the unique type name of our custom node. Mainly for mel purposes.
		static const MString typeName;

		static MObject colorR;
		static MObject colorG;
		static MObject colorB;
	};


#endif
