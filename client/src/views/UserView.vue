<script setup>
import {computed, ref, onBeforeMount, watch} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserProfileStore from '@/stores/UserProfileStore';

const userProfileStore = useUserProfileStore();
const {
  is_auth, 
  username, 
  is_superuser
} = storeToRefs(userProfileStore);

let cars = ref([]);
let photoinfo = ref([]);
let carsCount = ref();

let photoURI = ref();
let currentId = ref();

let photoRefForEdit = ref();

async function fetchCarsCount()
{
  const r = await axios.get("/api/cars/");

  cars.value = r.data;
  cars = cars.value.filter(item => item.username == username.value);
  carsCount = cars.length;
  console.log(carsCount);
}

async function fetchUserPhoto()
{
  const r = await axios.get("/api/user_photo/");

  photoinfo.value = r.data;
  
  photoinfo.value.forEach(item => {
    console.log(item.username == username.value);
    if (item.username == username.value)
    {
        photoURI = item.picture;
        currentId = item.id;
    }
  })

  console.log(username.value);
}

onBeforeMount(async () => {
  await fetchCarsCount();
  await fetchUserPhoto();
})

function photoEditPictureChange()
{
    photoURI.value = URL.createObjectURL(photoRefForEdit.value.files[0]);
}

async function onPhotoUpdateClick()
{
    const formData = new FormData();

    formData.append('picture', photoRefForEdit.value.files[0]);
    formData.set('username', username.value);

    await axios.put(`/api/user_photo/${currentId}/`, formData, {
        headers: {
        'Content-Type': 'multipart/form-data'
        }
    });

    await fetchUserPhoto();
}

</script>

<template>

<div class="modal fade" id="editPhotoModal" role="dialog" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">
                Редактировать фото пользователя
                </h1>
                <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
                ></button>
            </div>
            <div class="col-auto">
              <input class="form-control" type="file" ref="photoRefForEdit" @change="photoEditPictureChange">
            </div>
            <div class="col-auto">
              <img :src="photoURI" style="max-height: 60px" alt="">
            </div>
            <div class="modal-footer">
                <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
                >
                Close
                </button>
                <button
                data-bs-dismiss="modal"
                type="button"
                class="btn btn-primary"
                @click="onPhotoUpdateClick"
                >
                Сохранить
                </button>
            </div>
        </div>
    </div>
</div>

    <div class="Row">
        <div class="pair"> 
            <div class="ImageBlock" v-show="photoURI">
                <img class="img" :src="photoURI" alt="ава">
            </div>
            <div class="button-container">
                <button
                type="button"
                class="btn btn-secondary"
                @click="onPhotoEditClick"
                data-bs-toggle="modal"
                data-bs-target="#editPhotoModal"
                ><i class="bi bi-pen-fill"></i></button>
            </div>
        </div>
        <div class="infoBlock"> 
            <div class="infoItem">
                <div v-if="is_superuser">
                    <span class="header">Администратор</span>
                </div>
                <div v-else>
                    <span class="header">Обычный пользователь</span>
                </div>
            </div>
            <div class="infoItem">
                <span class="header">Имя: </span>{{ username }}
            </div>
            <div class="infoItem">
                <span class="header">Автомобилей: </span>{{ carsCount }}
            </div>
        </div>
    </div>
</template>

<style scoped>
.pair{
    position: relative;
    min-width: 400px;
    /*height: 400px;*/
}
.button-container {
  position: absolute;
  bottom: 10px;
  right: 10px;
}
.ImageBlock{
    max-width: 400px;
    max-height: 400px;
    border-radius: 50%;
    overflow: hidden;
}
.img{
    display: block;
    width: 100%;
}
.Row{
    display: flex;
    flex-direction: row;
    /*justify-content: center;*/
    align-items: center;

    margin-top: 40px;
    padding-left: 30px;
    padding-right: 30px;
}
.infoBlock{
    margin-left: 30px;
    padding: 20px 40px 20px 40px;
    
    width: 100%;

    border-radius: 20px;
    background-color: #A0D2EB;

    display: flex;
    flex-direction: column;
}
.infoItem{
    text-align: left;
    font-size: 28px;
}
.header{
  font-weight: bold;
}
</style>