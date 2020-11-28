#include <bits/stdc++.h>
using namespace std;

int  main():
    Image image = Image.open('rainbow.png');
    pixels = image.load();
    int width = image.width;
    int height=image.height;

    OctreeQuantizer octree();

    // add colors to the octree
    for (int j=0;j<height; j++){
        for (int i=0;i<width; i++){
            octree.add_color(Color(*pixels[i, j]))
        }
    }


    //256 colors for 8 bits per pixel output image
    vector <Color> palette = octree.make_palette(256)

    // create palette for 256 color max and save to file

    Image palette_image = Image.new('RGB', (16, 16))
    palette_pixels = palette_image.load()
    for(int i=0;i<palette.size();i++){
    	palette_pixels[i % 16, i / 16] = (color.red, color.green, color.blue);
    }
    palette_image.save('rainbow_palette.png')
    /*
    for i, color in enumerate(palette):
        palette_pixels[i % 16, i / 16] = (color.red, color.green, color.blue)
    palette_image.save('rainbow_palette.png')
	*/
    // save output image
    Image out_image = Image.new('RGB', (width, height))
    out_pixels = out_image.load()
    for (int j=0;j<height;j++){
        for (int i=0;i<width;i++){
            int index = octree.get_palette_index(Color(*pixels[i, j]))
            Color color = palette[index]
            out_pixels[i, j] = (color.red, color.green, color.blue)
    }
}
    out_image.save('rainbow_out.png')

/*
if __name__ == '__main__':
    main()
*/