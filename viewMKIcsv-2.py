import flet as ft

def on_file_open(e: ft.FilePickerResultEvent):
    print(f'Selected files: {e.files}')
    print(f'File path:      {e.path}')
    t.value = e.files
    e.page.update

def upload_files(e):
    upload_list = []
    if file_picker.result != None and file_picker.result.files != None:
        for f in file_picker.result.files:
            upload_list.append(
                FilePickerUploadFile(
                    f.name,
                    upload_url=page.get_upload_url(f.name, 600),
                )
            )
        file_picker.upload(upload_list)



def main (page: ft.Page):
    page.scroll = 'always'
    file_picker = ft.FilePicker(on_result=on_file_open)
    page.overlay.append(file_picker)
    t = ft.Text(value="Hello, world!", color="green")
    page.controls.append(t)
    file_btn = ft.ElevatedButton("Upload", on_click=upload_files)

    # file_btn = ft.ElevatedButton("Choose CSV files from MKI Yokogawa IAS...", on_click=lambda _: file_picker.pick_files())
    page.controls.append(file_btn)
    

    # if file_btn:
    #     t.value = 'file selected'
    #     page.update()
    
    page.update()
    

ft.app(target=main)