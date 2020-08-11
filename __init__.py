import numpy as np
class bmpFiler():

    COLOR_MODE_RGB = 1
    COLOR_MODE_BGR = 2
    COLOR_MODE_RGBA = 3
    COLOR_MODE_BGRA = 4


    raw_data = lambda w, h, b:b*w*h+(w%4)*h

    def create_bitmap_data(color_grid, padding, color_mode):
        if(color_mode == 1):
            #FLIP COLORS
            color_grid = np.flip(color_grid, 2)
        elif(color_mode == 3):
            #FLIP COLORS
            color_grid[:, :, 0], color_grid[:, :, 2] = color_grid[:, :, 2].copy(), color_grid[:, :, 0].copy()

        #FLIP FROM BOTTOM LINE TO TOP
        color_grid = np.flip(color_grid, 0)

        
        if(color_mode == 1 or color_mode == 2):
            #SPLIT COLORS
            color_grid = color_grid.reshape(color_grid.shape[0], color_grid.shape[1]*color_grid.shape[2], 1)
            #ADD PADDING only(RGB, BGR)
            for _ in range(padding):
                color_grid = np.insert(color_grid, color_grid.shape[1], [0], axis=1)
        
        #MERGE INTO ONE ARRAY
        color_grid = color_grid.reshape((color_grid.shape[0]*color_grid.shape[1]*color_grid.shape[2]))
        return bytes(color_grid)

    def generate_bmp_header(raw_data, color_mode):
        offset = 54
        if(color_mode == bmpFiler.COLOR_MODE_RGBA or color_mode == bmpFiler.COLOR_MODE_BGRA):
            offset = 122

        id_field = b'\x42\x4d'
        bmp_file_size = (offset+raw_data).to_bytes(4, byteorder="little")
        asp = b'\x00\x00\x00\x00'
        offset = (offset).to_bytes(4, byteorder="little")
        
        return id_field+bmp_file_size+asp+offset

    def generate_dib_header(color_mode, shape, raw_data):
        dim_bytes, bits, bi_rgb = b'', b'', b''
        
        red_mask, green_mask, blue_mask, alpha_mask = b'', b'', b'', b''
        lcs_windows_color_space = b''
        ciexyztriple_color_space = b''
        red_gamma, green_gamma, blue_gamma = b'', b'', b''

        if  (color_mode == bmpFiler.COLOR_MODE_RGB or color_mode == bmpFiler.COLOR_MODE_BGR):
            dim_bytes = (40).to_bytes(4, byteorder="little")
            bits = b'\x18\x00'
            bi_rgb = b'\x00\x00\x00\x00'
        elif(color_mode == bmpFiler.COLOR_MODE_RGBA or color_mode == bmpFiler.COLOR_MODE_BGRA):
            dim_bytes = (108).to_bytes(4, byteorder="little")
            bits = b'\x20\x00'
            bi_rgb = b'\x03\x00\x00\x00'

            red_mask, green_mask, blue_mask, alpha_mask = b'\x00\x00\xff\x00', b'\x00\xff\x00\x00', b'\xff\x00\x00\x00', b'\x00\x00\x00\xff'
            lcs_windows_color_space = b'\x20\x6e\x69\x57'
            ciexyztriple_color_space = b'\x00'*36
            red_gamma, green_gamma, blue_gamma = b'\x00'*4, b'\x00'*4, b'\x00'*4


        width = shape[0].to_bytes(4, byteorder="little")
        height = shape[1].to_bytes(4, byteorder="little")
        plane = b'\x01\x00'
        raw_data_hex = raw_data.to_bytes(4, byteorder="little")
        prt_res = (2835).to_bytes(4, byteorder="little")*2 
        palette = b'\x00\x00\x00\x00'
        important_colors = b'\x00\x00\x00\x00'
        
        shared_ = dim_bytes+width+height+plane+bits+bi_rgb+raw_data_hex+prt_res+palette+important_colors
        alph_ = red_mask+green_mask+blue_mask+alpha_mask+lcs_windows_color_space+ciexyztriple_color_space+red_gamma+green_gamma+blue_gamma
        return shared_+alph_
       

        
    def make_file(color_grid, color_mode=1, path="", name="test"):
        color_grid = np.array(color_grid)
        h, w, _ = color_grid.shape
        raw_data = 0
        if(color_mode == 1 or color_mode == 2):
            raw_data = bmpFiler.raw_data(w, h, 3)
        elif(color_mode == 3 or color_mode == 4):
            raw_data = bmpFiler.raw_data(w, h, 4)


        bmp_header = bmpFiler.generate_bmp_header(raw_data, color_mode)

        dib_header = bmpFiler.generate_dib_header(color_mode, (w, h), raw_data)
        
        bitmap_data = bmpFiler.create_bitmap_data(color_grid, w%4 if(color_mode == 1 or color_mode == 2) else 0, color_mode)
 
        with open("{}.bmp".format(name), "wb") as f:
            f.write(bmp_header+dib_header+bitmap_data)
            f.close()
