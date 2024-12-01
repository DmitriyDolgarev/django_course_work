<script setup>
import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const marks = ref([]);
const markToAdd = ref([]);
const markToEdit = ref([]);

let marksCount = ref();
let mostPopularMark = ref();

async function fetchMarks()
{
  const r_marks = await axios.get("/api/marks/");
  const r_stats = await axios.get("/api/cars/stats/");
  const r_marks_stats = await axios.get("/api/marks/stats/");

  let stats = r_stats.data;
  mostPopularMark = stats.most_mark_name;

  let marks_stats = r_marks_stats.data;
  marksCount = marks_stats.count;

  marks.value = r_marks.data;

  console.log(marks.value);
}

onBeforeMount(async () => {
  await fetchMarks();
})

async function onMarkAdd() {
  console.log(markToAdd.value);
  await axios.post("/api/marks/", {
    ...markToAdd.value,
  });
  
  await fetchMarks(); // переподтягиваю
}

async function onMarkEditClick(mark)
{
  markToEdit.value = { ...mark };
}

async function onUpdateMark()
{
  console.log(markToEdit.value);
  await axios.put(`/api/marks/${markToEdit.value.id}/`, {
    ...markToEdit.value,
  });
  await fetchMarks();
}

async function onRemoveClick(mark) {
  await axios.delete(`/api/marks/${mark.id}/`);
  await fetchMarks(); // переподтягиваю
}

</script>

<template>

        <form @submit.prevent.stop="onMarkAdd">
            <div class="row">
                <div class="col">
                <div class="form-floating">
                    <input
                    type="text"
                    class="form-control"
                    v-model="markToAdd.name"
                    required
                    />
                    <label for="floatingInput">Марка</label>
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
                                v-model="markToEdit.name"
                            />
                            <label for="floatingInput">Марка</label>
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
                        @click="onUpdateMark"
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
              <div class="statsHeader">{{ marksCount }}</div>
              <h6>Количество марок</h6>
            </div>
            <div class="statsItem second">
              <div class="statsHeader">{{ mostPopularMark }}</div>
              <h6>Самая популярная марка</h6>
            </div>
          </div>
        </div>

        <div v-for="item in marks" class="item">
            {{ item.name }}
            <button class="btn btn-danger" @click="onRemoveClick(item)">
              <i class="bi bi-x"></i>
            </button>
            <button
            type="button"
            class="btn btn-success"
            @click="onMarkEditClick(item)"
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