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

async function fetchBodyTypes()
{
  const r_body_types = await axios.get("/api/body-types/");

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

<div v-for="item in body_types" class="item">
    {{ item.name }}
    <div v-show="item.picture"><img :src="item.picture" style="max-height: 60px;" alt=""></div>
    <button class="btn btn-danger" @click="onRemoveClick(item)">
        Удалить
    </button>
    <button
    type="button"
    class="btn btn-success"
    @click="onBodyTypeEditClick(item)"
    data-bs-toggle="modal"
    data-bs-target="#editMarkModal"
    >
        Редактировать
    </button>
</div>

</template>

<style scoped>

.item{
  margin: 10px;
  padding: 5px 20px;
  border: 1px solid black;
  border-radius: 15px;

  display: grid;
  grid-template-columns: 5fr 1fr 1fr 1fr;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}

</style>