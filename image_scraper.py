import requests
from bs4 import BeautifulSoup
import os
from imgaug import augmenters as iaa


def image_download(url, folder, site):
   if not os.path.isdir(os.path.join(os.getcwd(), folder)):
      os.mkdir(os.path.join(os.getcwd(), folder))
   os.chdir(os.path.join(os.getcwd(), folder))
   r = requests.get(url)
   soup = BeautifulSoup(r.text, 'html.parser')
   images = soup.find_all('img')
   count = 0
   for im in images:
      print(im)
      name = im['src'].split("/")[-1]
      if ".jpg" in name:
         name = name.split(".jpg")[0]
      link = im['src']
      if link[0] != "h":
         link = site + link
      with open(name+'.jpg', 'wb') as f:
         if link[0] == "/":
            continue
         else:
            image = requests.get(link)
            f.write(image.content)
   os.chdir('..')

def augment_images():
   seq = iaa.Sequential([
      iaa.Crop(px=(0, 16)), # crop images from each side by 0 to 16px (randomly chosen)
      iaa.Fliplr(0.5), # horizontally flip 50% of the images
      iaa.GaussianBlur(sigma=(0, 3.0)) # blur images with a sigma of 0 to 3.0
   ])
   for file in os.list_dir('./pollock_images'):
      print(file)

def main():
   pollock_url = "https://www.jackson-pollock.org/jackson-pollock-paintings.jsp"
   rothko_url = "https://www.mark-rothko.org/mark-rothko-paintings.jsp"
   kooning_url = "https://www.dekooning.org/the-artist/artworks/view/all?view_all=1"
   #image_download(pollock_url, "pollock_images", "https://www.jackson-pollock.org/")
   #image_download(rothko_url, "rothko_images", "https://www.mark-rothko.org/")
   #image_download(kooning_url,"kooning_images", "https://www.dekooning.org/")
   augment_images()
   

if __name__ == "__main__":
   main()