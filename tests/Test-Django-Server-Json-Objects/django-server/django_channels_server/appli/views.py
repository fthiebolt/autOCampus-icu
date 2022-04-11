from time import sleep
from django.shortcuts import render
from numpy import array, size
from channels import Group
import json

def user_list(request):
    return render(request, 'carte/public/index.html')
iteration = array([[1.4656, 43.5617],
            [1.4657, 43.5616],
            [1.4658, 43.5614],
            [1.466, 43.5613],
            [1.4661, 43.5612],
            [1.4661, 43.5611],
            [1.4662, 43.561],
            [1.4663, 43.5609],
            [1.4664, 43.5609]])
size = size(iteration, 0) - 1

def send_coord():
    print(size)
    for i in range(0, size):
        Group('users').send({
                'text': json.dumps({
                "id": 'R1',
                "Lag": iteration[i][0],
                "Lat": iteration[i][1]
            })
        })
        sleep(1)
