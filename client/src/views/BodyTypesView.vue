<script setup>

import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const body_types = ref([]);
const body_typeToAdd = ref([]);
const body_typeToEdit = ref([]);

const bodyTypesPictureRef = ref();
const bodyTypesPictureRefForEdit = ref();
const bodyTypeAddImageUrl = ref();
const bodyTypeEditImageUrl = ref();

let bodyTypesCount = ref();
let mostPopularBodyType = ref();

async function fetchBodyTypes()
{
  const r_body_types = await axios.get("/api/body-types/");
  const r_stats = await axios.get("/api/cars/stats/");
  const r_bodyTypes_stats = await axios.get("/api/body-types/stats/");

  let stats = r_stats.data;
  mostPopularBodyType = stats.most_body_type;

  let bodyTypes_stats = r_bodyTypes_stats.data;
  bodyTypesCount = bodyTypes_stats.count;

  body_types.value = r_body_types.data;

  console.log(body_types.value);
}

onBeforeMount(async () => {
  await fetchBodyTypes();
})

async function onBodyTypeAdd() {
  const formData = new FormData();

  formData.append('picture', bodyTypesPictureRef.value.files[0]);
  formData.set('name', body_typeToAdd.value.name);

  console.log(formData.value);

  await axios.post("/api/body-types/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  await fetchBodyTypes(); // переподтягиваю
}

async function bodyTypesAddPictureChange()
{
  bodyTypeAddImageUrl.value = URL.createObjectURL(bodyTypesPictureRef.value.files[0]);
}

async function bodyTypesEditPictureChange()
{
  bodyTypeEditImageUrl.value = URL.createObjectURL(bodyTypesPictureRefForEdit.value.files[0]);
}

async function onBodyTypeEditClick(body_type)
{
  body_typeToEdit.value = { ...body_type };
  bodyTypeEditImageUrl.value = body_type.picture;
}

async function onBodyTypeUpdateClick()
{
  const formData = new FormData();

  formData.append('picture', bodyTypesPictureRefForEdit.value.files[0]);
  formData.set('name', body_typeToEdit.value.name);

  console.log(formData.value);

  await axios.put(`/api/body-types/${body_typeToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  await fetchBodyTypes();
}

async function onRemoveClick(body_type) {
  await axios.delete(`/api/body-types/${body_type.id}/`);
  await fetchBodyTypes(); // переподтягиваю
}

</script>

<template>

<form @submit.prevent.stop="onBodyTypeAdd">
    <div class="row">
        <div class="col">
          <div class="form-floating">
              <input
              type="text"
              class="form-control"
              v-model="body_typeToAdd.name"
              required
              />
              <label for="floatingInput">Тип кузова</label>
          </div>
        </div>
        <div class="col-auto">
          <input class="form-control" type="file" ref="bodyTypesPictureRef" @change="bodyTypesAddPictureChange">
        </div>
        <div class="col-auto">
          <img :src="bodyTypeAddImageUrl" style="max-height: 60px" alt="">
        </div>
        <div class="col-1">
        <button class="btn btn-primary">
            Добавить
        </button>
        </div>
    </div>
</form>

<div class="modal fade" id="editMarkModal" role="dialog" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">
                Редактировать
                </h1>
                <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
                ></button>
            </div>
            <div class="modal-body">
                <div class="row">
                <div class="col">
                    <div class="form-floating">
                    <input
                        type="text"
                        class="form-control"
                        v-model="body_typeToEdit.name"
                    />
                    <label for="floatingInput">Тип кузова</label>
                    </div>
                </div>
                </div>
            </div>
            <div class="col-auto">
              <input class="form-control" type="file" ref="bodyTypesPictureRefForEdit" @change="bodyTypesEditPictureChange">
            </div>
            <div class="col-auto">
              <img :src="bodyTypeEditImageUrl" style="max-height: 60px" alt="">
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
                @click="onBodyTypeUpdateClick"
                >
                Сохранить
                </button>
            </div>
        </div>
    </div>
</div>

<div class="stats">
  <h3>Статистика</h3>
  <div class="statsRow">
    <div class="statsItem first">
      <div class="statsHeader">{{ bodyTypesCount }}</div>
      <h6>Количество типов кузовов</h6>
    </div>
    <div class="statsItem second">
      <div class="statsHeader">{{ mostPopularBodyType }}</div>
      <h6>Самый популярный тип кузова</h6>
    </div>
  </div>
</div>

<div v-for="item in body_types" class="item">
    {{ item.name }}
    <div v-show="item.picture"><img :src="item.picture" style="max-height: 60px;" alt=""></div>
    <button class="btn btn-danger" @click="onRemoveClick(item)">
      <i class="bi bi-x"></i>
    </button>
    <button
    type="button"
    class="btn btn-success"
    @click="onBodyTypeEditClick(item)"
    data-bs-toggle="modal"
    data-bs-target="#editMarkModal"
    >
    <i class="bi bi-pen-fill"></i>
    </button>
</div>

</template>

<style scoped>

.item{
  margin: 15px;
  padding: 5px 20px;
  box-shadow: 10px 5px 5px rgba(128, 128, 128, 0.689);
  border-radius: 15px;

  display: grid;
  grid-template-columns: 14fr 4fr 1fr 1fr;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}

.stats{
  margin: 30px;
}
.statsRow{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}
.statsItem{
  margin: 20px;
  padding: 40px;
  border-radius: 15px;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.first{
  background-color: #FFF685;
}
.second{
  background-color: #FFABD6;
}
.third{
  background-color: #A0D2EB;
}
.statsHeader{
  font-size: 40px;
  font-weight: bold;
}

</style>