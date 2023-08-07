import os
import uuid
import re

def generate_guid():
    return str(uuid.uuid4()).upper()

def sanitize_id(text):
    sanitized = re.sub(r'[^A-Za-z0-9_.]', '_', text)
    return sanitized[:72]  # Limit identifier length to 72 characters

def generate_component(file_path, existing_ids):
    file_name = os.path.basename(file_path)
    component_guid = generate_guid()
    file_id = sanitize_id(os.path.splitext(file_name)[0])
    
    i = 1
    while file_id in existing_ids:
        file_id = sanitize_id(os.path.splitext(file_name)[0] + str(i))
        i += 1
    existing_ids.add(file_id)
    
    component = f"""
        <Component Id="{file_id}" Guid="{component_guid}">
          <File Id="{file_id}" Source="{file_path}" KeyPath="yes"/>
        </Component>
    """
    return component

def generate_directory(path, indent="", existing_ids=None):
    dir_name = os.path.basename(path)
    dir_id = sanitize_id(dir_name)
    
    i = 1
    while dir_id in existing_ids:
        dir_id = sanitize_id(dir_name + str(i))
        i += 1
    existing_ids.add(dir_id)
    
    components = ""
    subdirectories = ""
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            component_id = sanitize_id(os.path.splitext(item)[0])
            i = 1
            while component_id in existing_ids:
                component_id = sanitize_id(os.path.splitext(item)[0] + str(i))
                i += 1
            components += generate_component(item_path, existing_ids)
            existing_ids.add(component_id)
        elif os.path.isdir(item_path):
            subdirectories += generate_directory(item_path, indent + " ", existing_ids)
    
    directory = f"""
{indent}<Directory Id="{dir_id}" Name="{dir_name}">
{components}{subdirectories}
{indent}</Directory>
    """
    return directory

if __name__ == "__main__":
    package_name = input("Package Name: ")
    package_version = input("Version: ")
    package_manufacturer = input("Owner: ")
    
    start_path = input("Path: ")
    existing_ids = set()
    xml_output = generate_directory(start_path, existing_ids=existing_ids)
    
    root_path = os.path.abspath(start_path)
    component_refs = ""
    for line in xml_output.splitlines():
        if "<File Id=" in line:
            file_path = line.split('Source="')[1].split('"')[0]
            absolute_path = os.path.abspath(os.path.join(root_path, file_path))
            component_id = sanitize_id(line.split('"')[1])
            component_refs += f"      <ComponentRef Id=\"{component_id}\"/>\n"
    
    output_file_path = "output.wxs"
    with open(output_file_path, "w") as output_file:
        output_file.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Package Name="{package_name}" Version="{package_version}" Manufacturer="{package_manufacturer}" Language="1033" UpgradeCode="C3F6D7E8-9A4B-11EC-BF4C-0242AC130002">
    <Media Id="1" Cabinet="product.cab" EmbedCab="yes"/>
    <StandardDirectory Id="TARGETDIR" />
    <Directory Id="LocalAppDataFolder">
      <Directory Id="INSTALLFOLDER" Name="{package_name}">
{xml_output}
        </Directory>
    </Directory>
    <Feature Id="ProductFeature" Title="{package_name}" Level="1">
      <ComponentGroupRef Id="ProductComponents"/>
    </Feature>
  </Package>

  <Fragment>
    <Directory Id="ProgramMenuFolder">
      <Directory Id="ApplicationProgramsFolder" Name="{package_name}"/>
    </Directory>
  </Fragment>

  <Fragment>
    <ComponentGroup Id="ProductComponents">
{component_refs}
    </ComponentGroup>
  </Fragment>
</Wix>
        ''')
    
    print(f"Arquivo '{output_file_path}' foi gerado com sucesso!")
