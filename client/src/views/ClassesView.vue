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

let classesCount = ref();
let mostPopularClass = ref();

async function fetchClasses()
{
  const r_classes = await axios.get("/api/car-classes/");
  const r_stats = await axios.get("/api/cars/stats/");
  const r_classes_stats = await axios.get("/api/car-classes/stats/");

  let stats = r_stats.data;
  let text = stats.most_class;
  mostPopularClass = text[0];

  let classes_stats = r_classes_stats.data;
  classesCount = classes_stats.count;

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

<div class="stats">
  <h3>Статистика</h3>
  <div class="statsRow">
    <div class="statsItem first">
      <div class="statsHeader">{{ classesCount }}</div>
      <h6>Количество классов</h6>
    </div>
    <div class="statsItem second">
      <div class="statsHeader">{{ mostPopularClass }}</div>
      <h6>Самый популярный класс</h6>
    </div>
  </div>
</div>

<div v-for="item in classes" class="item">
    {{ item.name }}
    <button class="btn btn-danger" @click="onRemoveClick(item)">
      <i class="bi bi-x"></i>
    </button>
    <button
    type="button"
    class="btn btn-success"
    @click="onClassEditClick(item)"
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
  grid-template-columns: 17fr 1fr 1fr;
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