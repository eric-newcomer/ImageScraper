import requests
from bs4 import BeautifulSoup
import os
import sys
import imgaug as ia
from imgaug import augmenters as iaa
import cv2 as cv


def init_image_download():
   # Personal ".org" websites
   pollock_url = "https://www.jackson-pollock.org/jackson-pollock-paintings.jsp"
   rothko_url = "https://www.mark-rothko.org/mark-rothko-paintings.jsp"
   kooning_url = "https://www.dekooning.org/the-artist/artworks/view/all?view_all=1"
   
   # Art Net websites
   mitchell_url_recently_added = "http://www.artnet.com/artists/joan-mitchell/?type=paintings"
   mitchell_url_a_to_z = "http://www.artnet.com/artists/joan-mitchell/?type=paintings&sort=6"
   mitchell_url_z_to_a = "http://www.artnet.com/artists/joan-mitchell/?type=paintings&sort=7"
   mitchell_url_descending = "http://www.artnet.com/artists/joan-mitchell/?type=paintings&sort=12"
   newman_url_recently_added = "http://www.artnet.com/artists/barnett-newman/?type=paintings"
   newman_url_a_to_z = "http://www.artnet.com/artists/barnett-newman/?type=paintings&sort=6"
   newman_url_z_to_a = "http://www.artnet.com/artists/barnett-newman/?type=paintings&sort=7"
   newman_url_descending = "http://www.artnet.com/artists/barnett-newman/?type=paintings&sort=12"
   shiraga_url_recently_added = "http://www.artnet.com/artists/kazuo-shiraga/?type=paintings"
   shiraga_url_a_to_z = "http://www.artnet.com/artists/kazuo-shiraga/?type=paintings&sort=6"
   shiraga_url_z_to_a = "http://www.artnet.com/artists/kazuo-shiraga/?type=paintings&sort=7"
   shiraga_url_descending = "http://www.artnet.com/artists/kazuo-shiraga/?type=paintings&sort=12"

   image_download(pollock_url, "pollock_images", "https://www.jackson-pollock.org/")
   image_download(rothko_url, "rothko_images", "https://www.mark-rothko.org/")
   image_download(kooning_url,"kooning_images", "https://www.dekooning.org/")
  
   image_download(mitchell_url_recently_added, "mitchell_images", "http://www.artnet.com/artists/joan-mitchell/")
   image_download(mitchell_url_a_to_z, "mitchell_images", "http://www.artnet.com/artists/joan-mitchell/")
   image_download(mitchell_url_z_to_a, "mitchell_images", "http://www.artnet.com/artists/joan-mitchell/")
   image_download(mitchell_url_z_to_a, "mitchell_images", "http://www.artnet.com/artists/joan-mitchell/")
   
   image_download(newman_url_recently_added, "newman_images", "http://www.artnet.com/artists/barnett-newman/")
   image_download(newman_url_a_to_z, "newman_images", "http://www.artnet.com/artists/barnett-newman/")
   image_download(newman_url_z_to_a, "newman_images", "http://www.artnet.com/artists/barnett-newman/")
   image_download(newman_url_descending, "newman_images",  "http://www.artnet.com/artists/barnett-newman/")
   
   image_download(shiraga_url_recently_added, "shiraga_images", "http://www.artnet.com/artists/kazuo-shiraga/")
   image_download(shiraga_url_a_to_z, "shiraga_images", "http://www.artnet.com/artists/kazuo-shiraga/")
   image_download(shiraga_url_z_to_a, "shiraga_images", "http://www.artnet.com/artists/kazuo-shiraga/")
   image_download(shiraga_url_descending , "shiraga_images", "http://www.artnet.com/artists/kazuo-shiraga/")

   #clean_folders()



def image_download(url, folder, site=None):
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

def augment_images(dir):
   # Set image augmentation seed
   ia.seed(1)
   seq = iaa.Sequential([
      iaa.Crop(percent=(0, 0.1)), # crop images from each side by 0 to 10% (randomly chosen)
      iaa.Fliplr(0.5), # horizontally flip 50% of the images
       # Small gaussian blur with random sigma between 0 and 0.5.
      # But we only blur about 50% of all images.
      iaa.Sometimes(
         0.5,
         iaa.GaussianBlur(sigma=(0, 0.5))
      ),
       # Strengthen or weaken the contrast in each image.
    iaa.LinearContrast((0.75, 1.5))
   ], random_order=True)
   img_array = []
   for f in os.listdir("./"+dir):
      print(f)
      img = cv.imread(dir+"/"+f, cv.IMREAD_COLOR)
      cv.imshow("window", img)
      cv.waitKey()
      img_array.append(img)
   images_aug = seq(images=img_array)
   for im in images_aug:
      cv.imshow("aug", im)
      cv.waitKey()




def main(download=False):
   if download == True:
      init_image_download() 
   
   augment_images("shiraga_images")
   

if __name__ == "__main__":
   main()