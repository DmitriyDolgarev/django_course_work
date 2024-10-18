<script setup>

import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const countries = ref([]);
const countryToAdd = ref([]);
const countryToEdit = ref([]);

async function fetchCountries()
{
  const r_countries = await axios.get("/api/countries/");

  countries.value = r_countries.data;

  console.log(countries.value);
}

onBeforeMount(async () => {
  await fetchCountries();
})

async function onCountryAdd() {
  console.log(countryToAdd.value);
  await axios.post("/api/countries/", {
    ...countryToAdd.value,
  });
  
  await fetchCountries(); // переподтягиваю
}

async function onCountryEditClick(country)
{
  countryToEdit.value = { ...country };
}

async function onUpdateCountry()
{
  console.log(countryToEdit.value);
  await axios.put(`/api/countries/${countryToEdit.value.id}/`, {
    ...countryToEdit.value,
  });
  await fetchCountries();
}

async function onRemoveClick(country) {
  await axios.delete(`/api/countries/${country.id}/`);
  await fetchCountries(); // переподтягиваю
}

</script>

<template>

<form @submit.prevent.stop="onCountryAdd">
    <div class="row">
        <div class="col">
        <div class="form-floating">
            <input
            type="text"
            class="form-control"
            v-model="countryToAdd.name"
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
                        v-model="countryToEdit.name"
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
                @click="onUpdateCountry"
                >
                Сохранить
                </button>
            </div>
        </div>
    </div>
</div>

<div v-for="item in countries" class="item">
    {{ item.name }}
    <button class="btn btn-danger" @click="onRemoveClick(item)">
        Удалить
    </button>
    <button
    type="button"
    class="btn btn-success"
    @click="onCountryEditClick(item)"
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