import os
import shutil

packages_downloaded_folder = 'downloaded'
packages_result_folder = 'packages'

def extract_package_and_version():
    packages = []
    with open(os.path.join(packages_downloaded_folder, 'Packages'), 'r', encoding='utf-8') as f:
        # should run `dpkg-scanpackages . /dev/null > Packages`
        alltext = f.read()
        packages_raws = alltext.split('\n\n')
        packages_raws_splited = [p.split('\n') for p in packages_raws]
        for p in packages_raws_splited:
            package = {}
            for t in p:
                key = t[:t.find(':')].strip()
                value = t[t.find(':') + 1:].strip()
                if key != '' and value != '':
                    package[key] = value
            if 'Package' in package:
                packages.append(package)
    return packages

def get_new_packages_and_update_list(packages):
    package_raws = []
    with open('packages.list', 'r', encoding='utf-8') as f:
        alltext = f.read()
        package_raws = alltext.split('\n')

    package_raws = [x for x in package_raws if x.strip() != '']

    new_packages = []
    for p in packages:
        if package_raws.count(f"{p['Package']}={p['Version']}") == 0:
            new_packages.append(p)
            package_raws.append(f"{p['Package']}={p['Version']}")

    with open('packages.list', 'w', encoding='utf-8') as f:
        for p in package_raws:
            f.write(f"{p}\n")


    return new_packages

def copy_to_new(pkgs):
    os.makedirs(packages_result_folder, exist_ok=True)
    for p in pkgs:
        src = os.path.join(packages_downloaded_folder, p['Filename'])
        dest = os.path.join(packages_result_folder, p['Filename'])
        dest_dir = os.path.dirname(dest)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copyfile(src, dest)        

def main():
    pkgs = extract_package_and_version()
    new_pkgs = get_new_packages_and_update_list(pkgs)
    copy_to_new(new_pkgs)

main()
