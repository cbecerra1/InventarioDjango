#Se agregan estas dos lineas para que funcion y se debe ejecutar en entorno virtual
import sys
sys.path.append("..")

from config.wsgi import *
from erp.models import *
import random

# posgresql
# delete from public.erp_category;
# ALTER SEQUENCE erp_category_id_eq RESTART with 1;
# mysql
# alter table appinventario.erp_category AUTO_INCREMENT=1;

data = ['Leche y derivados', 'Carnes, pescados y huevos', 'Patatas, legumbres, frutos secos',
        'Verduras y Hortalizas', 'Frutas', 'Cereales y derivados, azúcar y dulces',
        'Grasas, aceite y mantequilla']

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for i in range(1, 6000):
        name = ''.join(random.choices(letters, k=5))
        while Category.objects.filter(name=name).exists():
                name = ''.join(random.choices(letters, k=5))
        Category(name=name).save()
        print('Guardado registro {}'.format(i))