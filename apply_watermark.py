import os
import PySimpleGUI as sg
# PySimpleGUI_License = 'eSy4JtMRa9WFNVljbVn2NjlMVqHglkw3ZNScIf6EIqkfRBl8dRm4Vws1b736B9lec0itIRseI1kYxCpvYr2WVwuLcX2GV8JtRGC1I36EMLTmcRyFM8zRgH3CN2TYUW4sN0ScwwiXTwGxldjcZNWg5PzHZfU4RElDcGG0xmvpeyWh1FlIbcneR3WKZAXBJ4zsaSWI9ZunI9jLo8xdLVCIJ3OZYqWe1Vl6RvmZlBy6ci3dQ2ikO5iCJvZfdSXjhY1CYgWW4Ji4LBCpJcOXYBWq17lUT5GtFxztdGCiIf6xICk8pEpVYzWW5MnmIzi6wCiQQT2V90tbcxGnFOudeZSFIj6qIpinINspIjkwN319cI3CRbvZbdWGV2yySgUqQhi3OaiqIvz5N6DTcJ43NjyrIdsgIfkLRAhrdTGYVZJ4cU38Nf1BZBWgQji7O0ipIXwyOmCT8axKNJy88myVMODQIE0cI7iWwtiaRRGdFQ0NZfUEVG4bcMGFlly1ZfXfMfi3OwiuIGwBOZCU8lxrN4yY8HyPM9D2IB1EIEiiwqi5R6WZ13hIa8W5xVB5ZEGRRRy9ZUXdNtzTIMjvoWifaHnilq42M5TPk351O9D1AJzeMADchoArZU2T1Mh0aVWkwNuFY62q9ztXIYiGw2iaSFVCBQB8ZuGNRRydZDXkNYz1I9juo7isOYTiYXusMujkQiyjL2jdUy0gLEjYkni9fDQ6=7=W6195fb56182bd3bca65d6dbcf27ff1dc6859d1f752a8477fd9ed51075d9347fa4e4a6943e322998d8da9135ec8c28604858bce42b4f6fe035bcd707ef367e6b07662ad28bd261745ed444f2799ea119fc01d0f0f093148e0bc02e7d7518b32f98dc4c8345a0127fc959e9e78f2802626831ba7dcaaa40f1ba2a719f733e90793aaed01881f744626429f48f0ac8a35989ded4b455675f875ffc834d90cbef0cae270992c098679e3cf9ba7cbb07c20238900658322543c1f8ea5185404adb124cbd4a3962402a766751d587b6dd8af4a637f34d70f27b2d6f77e90d25dc0a75fd3253f9d59d195e93f9e7592c87939c313adad21de3533da06fe70260393845dd79f3b7b6035fdfed0add9d7c3e97813e54d68c1806efe1e946c0fc4be79e121f0eefd3b846b4cdd5d049495e48f2f3296837766ace24e3385c73fbf27591c0c0af30040ce34c698ca548cdf90581efd393b2f81a3699fd14781be12657b250efefbc171165ae5d153a1fa6075cac00002fa0017e7b9fe938f7727aea6673f33476d388a0b6d92fb3707786c6fd175c63e5d7c3e03c5fead5064cd746f42306954ee21439b95303f4a74960a93195e61d25d655e816c2d7bd314b7c145278118bf25bf25260e9407f44e40143d57547b7f3e7bdbb55b177b9b3d57e35c673d70aea256ff5e2237bc2aa691fe4005aa629fba313f2741d9695b24bc097d68b83b'
from PIL import Image
import itertools

def apply_watermark(input_image_path, watermark_image_path, output_image_path, opacity=15, sub_scale=0.8):
    base_image = Image.open(input_image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")
    
    scale_factor = (base_image.width / watermark.width) * sub_scale
    new_size = (int(watermark.width * scale_factor), int(watermark.height * scale_factor))
    watermark = watermark.resize(new_size, Image.Resampling.LANCZOS)
    
    alpha_mask = watermark.split()[3].point(lambda p: p * opacity / 100)
    watermark.putalpha(alpha_mask)
    
    position = ((base_image.width - watermark.width) // 2, (base_image.height - watermark.height) // 2)
    
    watermarked_image = Image.alpha_composite(base_image, Image.new('RGBA', base_image.size))
    watermarked_image.paste(watermark, position, watermark)
    
    watermarked_image.convert("RGB").save(output_image_path, "PNG")

def watermark_all_photos(directory, watermark_image_path, output_directory, opacity=15, sub_scale=0.8, window=None):
    os.makedirs(output_directory, exist_ok=True)
    
    images = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_images = len(images)
    
    for i, filename in enumerate(images, start=1):
        input_image_path = os.path.join(directory, filename)
        output_image_path = os.path.join(output_directory, filename)
        apply_watermark(input_image_path, watermark_image_path, output_image_path, opacity, sub_scale)
        
        # Update the spinning icon
        window['spinner'].update(next(spin_sequence))
        
        # Update the progress meter
        sg.OneLineProgressMeter('Watermarking Progress', i, total_images, 'key', orientation='h')
        
    sg.popup('Watermarking Complete!')

# Define a spinning sequence for the icon using itertools.cycle
spin_sequence = itertools.cycle(['-', '\\', '|', '/'])

# Define the layout of the GUI
layout = [
    [sg.Text('Select Directory of Photos'), sg.Input(), sg.FolderBrowse(key='directory')],
    [sg.Text('Select Watermark Image'), sg.Input(), sg.FileBrowse(key='watermark_image')],
    [sg.Text('Select Output Directory'), sg.Input(), sg.FolderBrowse(key='output_directory')],
    [sg.Text('Opacity'), sg.Slider(range=(0, 100), orientation='h', size=(34, 20), default_value=15, key='opacity')],
    [sg.Text('Scale Factor'), sg.Slider(range=(0.1, 2.0), resolution=0.1, orientation='h', size=(34, 20), default_value=0.8, key='sub_scale')],
    [sg.Text('', size=(2, 1), key='spinner'), sg.Button('Watermark Photos'), sg.Button('Exit')]
]

# Create the window
window = sg.Window('Watermark Photos', layout)

# Event loop
while True:
    event, values = window.read(timeout=100)
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    if event == 'Watermark Photos':
        directory = values['directory']
        watermark_image_path = values['watermark_image']
        output_directory = values['output_directory']
        opacity = values['opacity']
        sub_scale = values['sub_scale']
        
        if directory and watermark_image_path and output_directory:
            watermark_all_photos(directory, watermark_image_path, output_directory, opacity, sub_scale, window=window)
        else:
            sg.popup('Please fill in all fields.')

# Close the window
window.close()