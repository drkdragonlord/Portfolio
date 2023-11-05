
//createNode jbMuscleCage;


#include "Locator.h"
#include <maya/MColor.h>
#include <maya/MLibrary.h>
#include <maya/MIOStream.h>
#include <maya/MGlobal.h>

int main(int /*argc*/, char **argv)
{
    MStatus status;

    status = MLibrary::initialize (true, argv[0], true);
    if ( !status ) {
        status.perror("MLibrary::initialize");
        return (1);
    }
    
    // Write the text out in 3 different ways.
	MGlobal::executeCommand( "global proc jbTestWinUI(){if(`window -ex $jbtestWin`)deleteUI $jbtestWin; string $jbtestWin =`window -w 200 -h 500`; showWindow $jbtestWin;jbTestWinUI();}", true );

    MLibrary::cleanup();

    return (0);
}

MObject jbMuscleCage::colorR;
MObject jbMuscleCage::colorG;
MObject jbMuscleCage::colorB;

const MTypeId jbMuscleCage::typeId( 0x70000 );
const MString jbMuscleCage::typeName( "jbMuscleCage" );

//------------------------------------------------------------------------
/// \brief	This function is used to render our custom locator node
/// \param	view	-	the maya viewport to render the locator node in
/// \param	DGpath	-	the DAG path of the object
/// \param	style	-
/// \param	status	-
///
void jbMuscleCage::draw( M3dView& view,
						  const MDagPath& DGpath,
						  M3dView::DisplayStyle style,
						  M3dView::DisplayStatus status )
{
	//MColor col(1.0, 0.0, 0.2);//= colorRGB( status );

	MObject thisNode = thisMObject();

	MPlug plugColorR( thisNode, colorR );
    float fColorR ;
    plugColorR.getValue( fColorR );

	MPlug plugColorG( thisNode, colorG );
    float fColorG ;
    plugColorR.getValue( fColorG );

	MPlug plugColorB( thisNode, colorB );
    float fColorB ;
    plugColorR.getValue( fColorB );

	// think glPushMatrix()
	view.beginGL();

	// this makes a copy of the current openGL settings so that anything
	// we change will not affect anything else maya draws afterwards.
	glPushAttrib( GL_CURRENT_BIT );

		// draw a red line
		MColor DefaultColor = colorRGB(status);
		
		if(status == M3dView::kLead )
			glColor3f(0.0f,0.7f,0.0f);
		else
			// Otherwise i use a slightly varied intensity of the colour
			//glColor3f(0.7f*DefaultColor.r,0.7f*DefaultColor.g,0.7f*DefaultColor.b);
			glColor3f(0.7f,0.0f,0.0f);

		glBegin(GL_LINE_STRIP); //GL_LINE_STRIP, GL_POINTS
		
				 //this makes the Z-axis ring
				 glVertex3f( 0.0f, 1.0f, 0.0f);
				 glVertex3f( 0.5f, 0.9f, 0.0f);				 
				 glVertex3f( 0.5f, 0.9f, 0.0f);
				 glVertex3f( 0.9f, 0.5f, 0.0f);				 
				 glVertex3f( 0.9f, 0.5f, 0.0f);
				 glVertex3f( 1.0f, 0.0f, 0.0f);
				 
				 glVertex3f( 1.0f, 0.0f, 0.0f);
				 glVertex3f( 0.9f, -0.5f, 0.0f);			 
				 glVertex3f( 0.9f, -0.5f, 0.0f);
				 glVertex3f( 0.5f, -0.9f, 0.0f);				 
				 glVertex3f( 0.5f, -0.9f, 0.0f);
				 glVertex3f( 0.0f, -1.0f, 0.0f);

				 glVertex3f( 0.0f, -1.0f, 0.0f);
				 glVertex3f( -0.5f, -0.9f, 0.0f);
				 glVertex3f( -0.5f, -0.9f, 0.0f);
				 glVertex3f( -0.9f, -0.5f, 0.0f);
				 glVertex3f( -0.9f, -0.5f, 0.0f);
				 glVertex3f( -1.0f, 0.0f, 0.0f);

				 glVertex3f( -1.0f, 0.0f, 0.0f);
				 glVertex3f( -0.9f, 0.5f, 0.0f);
				 glVertex3f( -0.9f, 0.5f, 0.0f);
				 glVertex3f( -0.5f, 0.9f, 0.0f);
				 glVertex3f( -0.5f, 0.9f, 0.0f);
				 glVertex3f( 0.0f, 1.0f, 0.0f);

				 //this makes the left diagonal ring
				 glVertex3f( 0.0f, 1.0f, 0.0f);
				 glVertex3f( 0.25f, 0.9f, 0.43f);
				 glVertex3f( 0.25f, 0.9f, 0.43f);
				 glVertex3f( 0.43f, 0.5f, 0.75f);
				 glVertex3f( 0.43f, 0.5f, 0.75f);
				 glVertex3f( 0.5f, 0.0f, 0.87f);

				 glVertex3f( 0.5f, 0.0f, 0.87f);
				 glVertex3f( 0.43f, -0.5f, 0.75f);
				 glVertex3f( 0.43f, -0.5f, 0.75f);
				 glVertex3f( 0.25f, -0.9f, 0.43f);
				 glVertex3f( 0.25f, -0.9f, 0.43f);
				 glVertex3f( 0.0f, -1.0f, 0.0f);

				 glVertex3f( 0.0f, -1.0f, 0.0f);
				 glVertex3f( -0.25f, -0.9f, -0.43f);
				 glVertex3f( -0.25f, -0.9f, -0.43f);
				 glVertex3f( -0.43f, -0.5f, -0.75f);
				 glVertex3f( -0.43f, -0.5f, -0.75f);
				 glVertex3f( -0.5f, 0.0f, -0.87f);

				 glVertex3f( -0.5f, 0.0f, -0.87f);
				 glVertex3f( -0.43f, 0.5f, -0.75f);
				 glVertex3f( -0.43f, 0.5f, -0.75f);
				 glVertex3f( -0.25f, 0.9f, -0.43f);
				 glVertex3f( -0.25f, 0.9f, -0.43f);
				 glVertex3f( 0.0f, 1.0f, 0.0f);

				 //this makes the right diagonal ring
				 glVertex3f( 0.0f, 1.0f, 0.0f);
				 glVertex3f( -0.25f, 0.9f, 0.43f);
				 glVertex3f( -0.25f, 0.9f, 0.43f);
				 glVertex3f( -0.43f, 0.5f, 0.75f);
				 glVertex3f( -0.43f, 0.5f, 0.75f);
				 glVertex3f( -0.5f, 0.0f, 0.87f);

				 glVertex3f( -0.5f, 0.0f, 0.87f);
				 glVertex3f( -0.43f, -0.5f, 0.75f);
				 glVertex3f( -0.43f, -0.5f, 0.75f);
				 glVertex3f( -0.25f, -0.9f, 0.43f);
				 glVertex3f( -0.25f, -0.9f, 0.43f);
				 glVertex3f( 0.0f, -1.0f, 0.0f);

				 glVertex3f( 0.0f, -1.0f, 0.0f);
				 glVertex3f( 0.25f, -0.9f, -0.43f);
				 glVertex3f( 0.25f, -0.9f, -0.43f);
				 glVertex3f( 0.43f, -0.5f, -0.75f);
				 glVertex3f( 0.43f, -0.5f, -0.75f);
				 glVertex3f( 0.5f, 0.0f, -0.87f);

				 glVertex3f( 0.5f, 0.0f, -0.87f);
				 glVertex3f( 0.43f, 0.5f, -0.75f);
				 glVertex3f( 0.43f, 0.5f, -0.75f);
				 glVertex3f( 0.25f, 0.9f, -0.43f);
				 glVertex3f( 0.25f, 0.9f, -0.43f);
				 glVertex3f( 0.0f, 1.0f, 0.0f);

				//this makes the top muscle cage ring 
				 glVertex3f( 0.5f, 0.9f, 0.0f);
				 glVertex3f( 0.25f, 0.9f, 0.43f);
				 glVertex3f( 0.25f, 0.9f, 0.43f);
				 glVertex3f( -0.25f, 0.9f, 0.43f);
				 glVertex3f( -0.25f, 0.9f, 0.43f);
				 glVertex3f( -0.5f, 0.9f, 0.0f);

				 glVertex3f( -0.5f, 0.9f, 0.0f);
				 glVertex3f( -0.25f, 0.9f, -0.43f);
				 glVertex3f( -0.25f, 0.9f, -0.43f);
				 glVertex3f( 0.25f, 0.9f, -0.43f);
				 glVertex3f( 0.25f, 0.9f, -0.43f);
				 glVertex3f( 0.5f, 0.9f, 0.0f);
				 
				 //this makes the top middle muscle cage ring
				 glVertex3f( 0.9f, 0.5f, 0.0f);
				 glVertex3f( 0.43f, 0.5f, 0.75f);
				 glVertex3f( 0.43f, 0.5f, 0.75f);
				 glVertex3f( -0.43f, 0.5f, 0.75f);
				 glVertex3f( -0.43f, 0.5f, 0.75f);
				 glVertex3f( -0.9f, 0.5f, 0.0f);

				 glVertex3f( -0.9f, 0.5f, 0.0f);
				 glVertex3f( -0.43f, 0.5f, -0.75f);
				 glVertex3f( -0.43f, 0.5f, -0.75f);
				 glVertex3f( 0.43f, 0.5f, -0.75f);
				 glVertex3f( 0.43f, 0.5f, -0.75f);
				 glVertex3f( 0.9f, 0.5f, 0.0f);

				 //this makes the middle muscle cage ring
				 glVertex3f( 1.0f, 0.0f, 0.0f);
				 glVertex3f( 0.5f, 0.0f, 0.87f);
				 glVertex3f( 0.5f, 0.0f, 0.87f);
				 glVertex3f( -0.5f, 0.0f, 0.87f);
				 glVertex3f( -0.5f, 0.0f, 0.87f);
				 glVertex3f( -1.0f, 0.0f, 0.0f);
				 
				 glVertex3f( -1.0f, 0.0f, 0.0f);
				 glVertex3f( -0.5f, 0.0f, -0.87f);
				 glVertex3f( -0.5f, 0.0f, -0.87f);
				 glVertex3f( 0.5f, 0.0f, -0.87f);
				 glVertex3f( 0.5f, 0.0f, -0.87f);
				 glVertex3f( 1.0f, 0.0f, 0.0f);

				 //this makes the bottom middle muscle cage ring
				 glVertex3f( 0.9f, -0.5f, 0.0f);
				 glVertex3f( 0.43f, -0.5f, 0.75f);
				 glVertex3f( 0.43f, -0.5f, 0.75f);
				 glVertex3f( -0.43f, -0.5f, 0.75f);
				 glVertex3f( -0.43f, -0.5f, 0.75f);
				 glVertex3f( -0.9f, -0.5f, 0.0f);

				 glVertex3f( -0.9f, -0.5f, 0.0f);
				 glVertex3f( -0.43f, -0.5f, -0.75f);
				 glVertex3f( -0.43f, -0.5f, -0.75f);
				 glVertex3f( 0.43f, -0.5f, -0.75f);
				 glVertex3f( 0.43f, -0.5f, -0.75f);
				 glVertex3f( 0.9f, -0.5f, 0.0f);

				//this makes the bottom muscle cage ring 
				 glVertex3f( 0.5f, -0.9f, 0.0f);
				 glVertex3f( 0.25f, -0.9f, 0.43f);
				 glVertex3f( 0.25f, -0.9f, 0.43f);
				 glVertex3f( -0.25f, -0.9f, 0.43f);
				 glVertex3f( -0.25f, -0.9f, 0.43f);
				 glVertex3f( -0.5f, -0.9f, 0.0f);

				 glVertex3f( -0.5f, -0.9f, 0.0f);
				 glVertex3f( -0.25f, -0.9f, -0.43f);
				 glVertex3f( -0.25f, -0.9f, -0.43f);
				 glVertex3f( 0.25f, -0.9f, -0.43f);
				 glVertex3f( 0.25f, -0.9f, -0.43f);
				 glVertex3f( 0.5f, -0.9f, 0.0f);

	glEnd();

/*		glColor3f(DefaultColor.r, DefaultColor.g, DefaultColor.b);
		glBegin(GL_LINE_STRIP); //GL_LINE_STRIP, GL_POINTS
				 glVertex3f( 0.0f, 0.0f, 1.0f);
				 glVertex3f( 0.0f, 0.0f, 3.0f);
				 glVertex3f( 0.0f, 1.0f, 3.0f);
				 glVertex3f( 0.0f, 3.0f, 5.0f);
				 glVertex3f( 0.0f, 4.0f, 4.0f);
				 glVertex3f( 0.0f, 4.0f, 2.0f);
				 glVertex3f( 0.0f, 7.0f, 1.0f);
				 glVertex3f( 0.0f, 9.0f, 2.0f);
				 glVertex3f( 0.0f, 11.0f, 0.0f);
				 glVertex3f( 0.0f, 9.0f, -2.0f);
				 glVertex3f( 0.0f, 7.0f, -1.0f);
				 glVertex3f( 0.0f, 4.0f, -2.0f);
				 glVertex3f( 0.0f, 4.0f, -4.0f);
				 glVertex3f( 0.0f, 3.0f, -5.0f);
				 glVertex3f( 0.0f, 1.0f, -3.0f);
				 glVertex3f( 0.0f, 0.0f, -3.0f);
				 glVertex3f( 0.0f, 0.0f, -1.0f);
				 glVertex3f( 0.0f, 1.0f, -1.0f);
				 glVertex3f( 0.0f, 3.0f, -3.0f);
				 glVertex3f( 0.0f, 3.0f, -1.0f);
				 glVertex3f( 0.0f, 5.0f, 0.0f);
				 glVertex3f( 0.0f, 3.0f, 1.0f);
				 glVertex3f( 0.0f, 3.0f, 3.0f);
				 glVertex3f( 0.0f, 1.0f, 1.0f);
				 glVertex3f( 0.0f, 0.0f, 1.0f);
				
		glEnd();
	*/
		// draw yellow quad on xz plane (going to alpha blend it so we can see through it,
		// which i reackon makes it a bit less obtrusive)
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);

		if(status == M3dView::kLead)
			glColor4f(1,0,0,0.2f);
		else
			glColor4f(0.0f, 0.0f, 0.7f, 0.2f);

		glBegin(GL_POLYGON);
					/*
					glVertex3f( -3.0f, 0.0f, -3.0f);
					glVertex3f( -3.0f, 0.0f, 3.0f);
					glVertex3f( 3.0f, 0.0f, 3.0f);
					glVertex3f( 3.0f, 0.0f, -3.0f);
					*/

					glVertex3f( 1.0f, 0.0f, 0.0f);
					glVertex3f( 0.5f, 0.0f, 0.87f);
					glVertex3f( 0.5f, 0.0f, 0.87f);
					glVertex3f( -0.5f, 0.0f, 0.87f);
					glVertex3f( -0.5f, 0.0f, 0.87f);
					glVertex3f( -1.0f, 0.0f, 0.0f);

					glVertex3f( -1.0f, 0.0f, 0.0f);
					glVertex3f( -0.5f, 0.0f, -0.87f);
					glVertex3f( -0.5f, 0.0f, -0.87f);
					glVertex3f( 0.5f, 0.0f, -0.87f);
					glVertex3f( 0.5f, 0.0f, -0.87f);
					glVertex3f( 1.0f, 0.0f, 0.0f);


							
		glEnd();
		glDisable(GL_BLEND);

	// restore the old openGL settings
	glPopAttrib();

	// think glPopMatrix()
	view.endGL();
}

//------------------------------------------------------------------------
/// \brief	this function can tell maya whether the locator node has a volume
/// \return	true if bounded, false otherwise.
///
bool jbMuscleCage::isBounded() const
{
	return true;
}

//------------------------------------------------------------------------
/// \brief	returns the bounding box of the locator node
/// \return	the nodes bounding box
///
MBoundingBox jbMuscleCage::boundingBox() const
{
	MBoundingBox bbox;

	// simply expand the bounding box to contain the points used
	bbox.expand( MPoint( -5.0f, 0.0f, -5.0f ) );
	bbox.expand( MPoint(  5.0f, 0.0f, -5.0f ) );
	bbox.expand( MPoint(  0.5f, 0.0f,  5.0f ) );
	bbox.expand( MPoint( -5.0f, 0.0f,  5.0f ) );
	bbox.expand( MPoint(  0.0f,-0.5f,  0.0f ) );
	bbox.expand( MPoint(  0.0f, 12.0f,  0.0f ) );

	return bbox;
}

//------------------------------------------------------------------------
/// \brief	this function is called by mata to return a new instance of our locator node
/// \return	the new node
///
void* jbMuscleCage::creator()
{
	return new jbMuscleCage();
	return new main();
}

//------------------------------------------------------------------------
/// \brief	this function creates a description of our node
/// \return	The status code
///
MStatus jbMuscleCage::initialize()
{	
	MFnNumericAttribute nAttr;
	MStatus				stat;

	colorR = nAttr.create( "colorR", "colR", MFnNumericData::kFloat, 0.0 );
	nAttr.setStorable(true);
	nAttr.setKeyable(true);

	colorG = nAttr.create( "colorG", "colG", MFnNumericData::kFloat, 0.0 );
	nAttr.setStorable(true);
	nAttr.setKeyable(true);

	colorB = nAttr.create( "colorB", "colB", MFnNumericData::kFloat, 0.0 );
	nAttr.setStorable(true);
	nAttr.setKeyable(true);

	addAttribute( colorR );
	addAttribute( colorG );
	addAttribute( colorB );

	return MS::kSuccess;
}
