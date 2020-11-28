// ConsoleApplication2.cpp : Este archivo contiene la función "main". La ejecución del programa comienza y termina ahí.
//
#include "pch.h"
#include <opencv2/opencv.hpp>
#include <vector>

using namespace cv;
using namespace std;
class Color
{
public:
	int red, green, blue, alpha;
	Color(int red = 0, int green = 0, int blue = 0, int alpha = 1)
	{
		this->red = red;
		this->green = green;
		this->blue = blue;
		this->alpha = alpha;
	}
};
class OctreeQuantizer;
class OctreeNode
{
public:
	int pixel_count, palette_index;
	Color color;
	vector<OctreeNode*>children;
	OctreeNode(int level, OctreeQuantizer *parent);
	//friend class OctreeQuantizer;
	bool is_leaf();
	vector<OctreeNode*>get_leaf_nodes();
	int get_nodes_pixel_count();
	int get_palette_index(Color color, int level);
	int remove_leaves();
	int get_color_index_for_level(Color color, int level);
	Color get_color();
	void add_color(Color color, int level, OctreeQuantizer *parent);

};

class OctreeQuantizer
{
public:

	int MAX_DEPTH = 8;
	OctreeNode *root;
	//friend class  OctreeNode;
	vector<vector<OctreeNode*>>levels;
	OctreeQuantizer()
	{
		this->levels.assign(this->MAX_DEPTH, {});
		this->root = new OctreeNode(0, this);
	}
	vector<OctreeNode*>get_leaves()
	{
		return this->root->get_leaf_nodes();
	}
	void add_level_node(int level, OctreeNode *node)
	{
		this->levels[level].push_back(node);
	}

	void add_color(Color color)
	{
		this->root->add_color(color,0,this);
	}
	vector<Color> make_palette(int color_count) {
		vector<Color> palette;
		int palette_index = 0;
		int leaf_count = this->get_leaves().size();
		for (int level = this->MAX_DEPTH - 1; level > -1; level -= 1) {
			if (this->levels[level].size() > 0) {
				for (auto node : this->levels[level]) {
					leaf_count -= node->remove_leaves();
					if (leaf_count <= color_count)
					{
						break;
					}
				}
				if (leaf_count <= color_count)
					break;
				this->levels[level].clear();
			}
		}
		for (auto node : this->get_leaves()) {
			if (palette_index >= color_count)
				break;
			if (node->is_leaf())
				palette.push_back(node->get_color());
			node->palette_index = palette_index;
			palette_index += 1;
		}
		return palette;
	}
	int get_palette_index(Color color)
	{
		return this->root->get_palette_index(color, 0);
	}
};

OctreeNode::OctreeNode(int level, OctreeQuantizer*parent)
{
	this->pixel_count = 0;
	this->palette_index = 0;
	this->color.red = 0;
	this->color.blue = 0;
	this->color.green = 0;
	this->children.resize(8);
	if (level < parent->MAX_DEPTH-1)
	{
		parent->add_level_node(level, this);
	}

}
bool OctreeNode::is_leaf()
{
	return this->pixel_count > 0;
}
vector<OctreeNode*>OctreeNode::get_leaf_nodes()
{
	
	vector<OctreeNode*>leaf_nodes;
	for (int i = 0; i < 8; i++)
	{
		OctreeNode *Node = this->children[i];
		if (Node != nullptr)
		{
			if (Node->is_leaf())
			{
				leaf_nodes.push_back(Node);
			}
			else
			{
				vector<OctreeNode*> vector2 = Node->get_leaf_nodes();
				leaf_nodes.insert(leaf_nodes.end(), vector2.begin(), vector2.end());
			}
		}

	}
	return leaf_nodes;
}
int OctreeNode::get_nodes_pixel_count()
{
	int sum_count;
	
	sum_count = this->pixel_count;
	for (int i = 0; i < 8; i++)
	{
		OctreeNode *Node = this->children[i];
		if (Node!=nullptr)
		{
			sum_count += Node->pixel_count;
		}
	}
	return sum_count;
}
int OctreeNode::get_palette_index(Color color, int level)
{
	if (this->is_leaf())
	{
		return this->palette_index;
	}
	int index = this->get_color_index_for_level(color, level);
	if (this->children[index])
	{
		return this->children[index]->get_palette_index(color, level + 1);
	}
	else
	{
		for (int i = 0; i < 8; i++)
		{
			if (this->children[i] != nullptr)
			{
				return this->children[i]->get_palette_index(color, level + 1);
			}
		}
	}
}
int OctreeNode::remove_leaves()
{
	int result = 0;
	
	for (int i = 0; i < 8; i++)
	{
		OctreeNode *Node;
		Node = this->children[i];
		if (Node!=nullptr)
		{
			this->color.red += Node->color.red;
			this->color.green += Node->color.green;
			this->color.blue += Node->color.blue;
			this->pixel_count += Node->pixel_count;
			result += 1;


		}
	}
	return result - 1;

}
int OctreeNode::get_color_index_for_level(Color color, int level)
{
	int index = 0;
	int mask = 0x80 >> level;
	if (color.red & mask)
	{
		index |= 4;
	}
	if (color.green & mask)
	{
		index |= 2;
	}
	if (color.blue & mask)
	{
		index |= 1;
	}
	return index;
}
Color OctreeNode::get_color()
{
	return Color(
		this->color.red / this->pixel_count, 
		this->color.green / this->pixel_count, 
		this->color.blue / this->pixel_count);
}
void OctreeNode::add_color(Color color, int level, OctreeQuantizer *parent)
{
	if (level >= parent->MAX_DEPTH)
	{
		this->color.red += color.red;
		this->color.green += color.green;
		this->color.blue += color.blue;
		this->pixel_count += 1;
		return;
	}
	int index = this->get_color_index_for_level(color, level);
	if (children[index] == nullptr)
	{
		this->children[index] = new OctreeNode(level, parent);
	}
	this->children[index]->add_color(color, level + 1, parent);
}

int main()
{
	Mat image = imread("rainbow.jpg");
	int width = image.rows;
	int height = image.cols;
	int palete = 4;
	int palette_size = sqrt(palete);

	OctreeQuantizer octree;

	for (int j = 0; j < height; j++) {
		for (int i = 0; i < width; i++) {
			octree.add_color(Color(image.at<cv::Vec3b>(i, j)[2], image.at<cv::Vec3b>(i, j)[1], image.at<cv::Vec3b>(i, j)[0]));
		}
	}

	vector<Color> palette = octree.make_palette(palete);

	Mat palette_pixels = Mat(palette_size, palette_size, CV_8UC3);
	cout << palette.size();
	for (int i = 0; i < palette.size(); i++) {
		palette_pixels.data[palette_pixels.step[0] * (i % palette_size) + palette_pixels.step[1] * (i / palette_size) + 0] = palette[i].blue;
		palette_pixels.data[palette_pixels.step[0] * (i % palette_size) + palette_pixels.step[1] * (i / palette_size) + 1] = palette[i].green;
		palette_pixels.data[palette_pixels.step[0] * (i % palette_size) + palette_pixels.step[1] * (i / palette_size) + 2] = palette[i].red;
	}
	imwrite("rainbow_palette.png", palette_pixels);

	Mat out_pixels = Mat(width, height, CV_8UC3);
	int index;
	for (int j = 0; j < height; j++) {
		for (int i = 0; i < width; i++) {
			index = octree.get_palette_index(Color(image.at<cv::Vec3b>(i, j)[2], image.at<cv::Vec3b>(i, j)[1], image.at<cv::Vec3b>(i, j)[0]));
			Color color = palette[index];
			out_pixels.data[out_pixels.step[0] * i + out_pixels.step[1] * j + 0] = color.blue;
			out_pixels.data[out_pixels.step[0] * i + out_pixels.step[1] * j + 1] = color.green;
			out_pixels.data[out_pixels.step[0] * i + out_pixels.step[1] * j + 2] = color.red;
		}
	}
	imwrite("rainbow_out.png", out_pixels);

	namedWindow("image", WINDOW_NORMAL);

	imshow("image", out_pixels);
	waitKey(0);
	return 0;
}

// Ejecutar programa: Ctrl + F5 o menú Depurar > Iniciar sin depurar
// Depurar programa: F5 o menú Depurar > Iniciar depuración

// Sugerencias para primeros pasos: 1. Use la ventana del Explorador de soluciones para agregar y administrar archivos
//   2. Use la ventana de Team Explorer para conectar con el control de código fuente
//   3. Use la ventana de salida para ver la salida de compilación y otros mensajes
//   4. Use la ventana Lista de errores para ver los errores
//   5. Vaya a Proyecto > Agregar nuevo elemento para crear nuevos archivos de código, o a Proyecto > Agregar elemento existente para agregar archivos de código existentes al proyecto
//   6. En el futuro, para volver a abrir este proyecto, vaya a Archivo > Abrir > Proyecto y seleccione el archivo .sln
