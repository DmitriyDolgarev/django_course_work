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

async function fetchMarks()
{
  const r_marks = await axios.get("/api/marks/");

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

        <div v-for="item in marks" class="item">
            {{ item.name }}
            <button class="btn btn-danger" @click="onRemoveClick(item)">
                Удалить
            </button>
            <button
            type="button"
            class="btn btn-success"
            @click="onMarkEditClick(item)"
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