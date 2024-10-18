<script setup>

import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const classes = ref([]);
const classToAdd = ref([]);
const classToEdit = ref([]);

async function fetchClasses()
{
  const r_classes = await axios.get("/api/car-classes/");

  classes.value = r_classes.data;

  console.log(classes.value);
}

onBeforeMount(async () => {
  await fetchClasses();
})

async function onClassAdd() {
  console.log(classToAdd.value);
  await axios.post("/api/car-classes/", {
    ...classToAdd.value,
  });
  
  await fetchClasses(); // переподтягиваю
}

async function onClassEditClick(clas)
{
  classToEdit.value = { ...clas };
}

async function onUpdateClass()
{
  console.log(classToEdit.value);
  await axios.put(`/api/car-classes/${classToEdit.value.id}/`, {
    ...classToEdit.value,
  });
  await fetchClasses();
}

async function onRemoveClick(clas) {
  await axios.delete(`/api/car-classes/${clas.id}/`);
  await fetchClasses(); // переподтягиваю
}

</script>

<template>

<form @submit.prevent.stop="onClassAdd">
    <div class="row">
        <div class="col">
        <div class="form-floating">
            <input
            type="text"
            class="form-control"
            v-model="classToAdd.name"
            required
            />
            <label for="floatingInput">Класс</label>
        </div>
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
                        v-model="classToEdit.name"
                    />
                    <label for="floatingInput">Класс</label>
                    </div>
                </div>
                </div>
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
                @click="onUpdateClass"
                >
                Сохранить
                </button>
            </div>
        </div>
    </div>
</div>

<div v-for="item in classes" class="item">
    {{ item.name }}
    <button class="btn btn-danger" @click="onRemoveClick(item)">
        Удалить
    </button>
    <button
    type="button"
    class="btn btn-success"
    @click="onClassEditClick(item)"
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
  grid-template-columns: 5fr 1fr 1fr;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}

</style>