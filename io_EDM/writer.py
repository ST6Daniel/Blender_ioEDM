
import bpy

import itertools
import os
from .edm.types import Material, VertexFormat, Texture, Node, RenderNode, RootNode
from .edm.mathtypes import Matrix

def write_file(filename, options={}):

  # Start by: Assembling the materials
  # Go through every object in the scene and grab it's first material
  # This will make sure that we only create materials that are used
  all_Materials = [obj.material_slots[0].material for obj in bpy.context.scene.objects]
  materialMap = {m.name: create_material(m) for m in all_Materials}
  materials = []
  for i, mat in enumerate(all_Materials):
    mat.index = i
    materials.append(mat)

  # Now, build each RenderNode object
  renderNodes = []
  for obj in [x for x in bpy.context.scene.objects if x.type == "MESH"]:
    material = materialMap[obj.material_slots[0].material.name]
    node = create_rendernode(obj, material)
    renderNodes.append(node)

  # Build the nodelist from the renderNode parents
  nodes = [Node()]
  for rn in renderNodes:
    if rn.parent = None:
      rn.parent = 0
    else:
      nodes.append(rn.parent)
      rn.parent = len(nodes)-1
    rn.material = rn.material.index

  # Materials:    √
  # Render Nodes: √
  # Parents:      √
  # Let's build the root node
  root = RootNode()
  root.nodes = nodes
  root.materials = materials
  # And finally the wrapper
  file = EDMFile()
  file.node = root
  file.renderNodes.append(renderNodes)

  with open(filename, 'wb') as f:
    file.write(f)
  
def create_texture(source):
  # Get the texture name stripped of ALL extensions
  texName = os.path.basename(source.texture.image.filepath)
  texName = texName[:texName.find(".")]
  
  # Work out the channel for this texture
  if source.use_map_color_diffuse:
    index = 0
  elif source.use_map_normal:
    index = 1
  elif source.use_map_specular:
    index = 2

  # For now, assume identity transformation until we understand
  matrix = Matrix()
  return Texture(index=index, name=texName, matrix=matrix)

def create_material(source):
  mat = Material()
  mat.blending = source.edm_blending
  mat.material_name = source.edm_material
  mat.name = source.name
  mat.uniforms = {
    "specFactor": source.specular_intensity,
    "specPower": source.specular_hardness
  }
  mat.vertex_format = VertexFormat({
    "position": 4,
    "normal": 3,
    "tex0": 2
    })
  mat.texture_coordinates_channels = [0] + [-1]*11
  # Find the textures for each of the layers
  # Find diffuse - this will sometimes also include a translucency map
  diffuseTex = [x for x in source.texture_slots if x.use_map_color_diffuse]
  # normalTex = [x for x in source.texture_slots if x.use_map_normal]
  # specularTex = [x for x in source.texture_slots if x.use_map_specular]

  assert len(diffuseTex) == 1
  mat.textures.append(create_texture(diffuseTex[0]))

  return mat

def create_rendernode(source, material):
  assert source.type == "MESH"

  mesh = source.data
  mesh.calc_tessface()

  # Should be more complicated for multiple layers, but will do for now
  uv_tex = mesh.tessface_uv_textures.active.data

  newVertices = []
  newIndexValues = []
  # Loop over every face, and the UV data for that face
  for face, uvFace in zip(mesh.tessfaces, uv_tex):
    # What are the new index values going to be?
    newFaceIndex = [len(newVertices)+x for x in range(len(face.vertices))]
    # Build the new vertex data
    for i, vtxIndex in enumerate(face.vertices):
      newVertices.append(tuple(itertools.chain(mesh.vertices[vtxIndex].co, [0], mesh.vertices[vtxIndex].normal, uvFace.uv[i])))

    # We either have triangles or quads. Split into triangles, based on the
    # vertex index subindex in face.vertices
    if len(face.vertices) == 3:
      triangles =  ((0, 1, 2),)
    else:
      triangles = ((0, 1, 2),(2, 3, 0))

    # Write each vertex of each triangle
    for tri in triangles:
      for i in tri:
        newIndexValues.append(newFaceIndex[i])

  node = RenderNode()
  node.name = source.name
  node.material = material
  node.vertexData = newVertices
  node.indexData = newIndexValues
  return node