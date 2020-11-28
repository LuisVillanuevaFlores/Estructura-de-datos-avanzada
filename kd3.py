import vtk

'''VTK'''
plane1 = vtk.vtkPlaneSource()
plane1.SetCenter(1.0, 0.0, 0.0)
plane1.SetNormal(1.0, 0.0, 0.0)
# planes.SetExtent(1,100,1,100,7,7);

'''VTK'''
plane2 = vtk.vtkPlaneSource()
plane2.SetCenter(1.0, 2.0, 0.0)
plane2.SetNormal(0.0, 1.0, 0.0)
# planes.SetExtent(1,100,1,100,7,7);

# mapper
mapper1 = vtk.vtkPolyDataMapper()
mapper1.SetInput(plane1.GetOutput())

# mapper
mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInput(plane2.GetOutput())

# actor
actor1 = vtk.vtkActor()
actor1.SetMapper(mapper1)

actor2 = vtk.vtkActor()
actor2.SetMapper(mapper2)


'''RENDER'''
renderer = vtk.vtkRenderer()
# Background
renderer.SetBackground(1., 1., 1.)
# Add actor to the scene
renderer.AddActor(actor1)
renderer.AddActor(actor2)

'''Render window'''
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

'''Interactor'''
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
renderWindowInteractor.SetRenderWindow(renderWindow)

'''Add camera coordinates'''
axes = vtk.vtkAxesActor()
widget = vtk.vtkOrientationMarkerWidget()
widget.SetOutlineColor(0.9300, 0.5700, 0.1300)
widget.SetOrientationMarker(axes)
widget.SetInteractor(renderWindowInteractor)
widget.SetViewport(0.0, 0.0, 0.4, 0.4)
widget.SetEnabled(1)
widget.InteractiveOn()

# Reset camera
renderer.ResetCamera()

'''Begin interaction'''
renderWindow.Render()
renderWindowInteractor.Initialize()
renderWindowInteractor.Start()
renderWindowInteractor.Start()
