<template>
    <div class="card p-4 mb-4 bg-white rounded-lg shadow">
        <h2 class="text-lg font-semibold mb-2">{{ title }}</h2>
        <Bar v-if="type === 'bar'" :data="chartData" :options="chartOptions" />
        <Line v-if="type === 'line'" :data="chartData" :options="chartOptions" />
    </div>
</template>

<script setup>
import { Bar, Line } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale, PointElement)

defineProps({
    title: String,
    chartData: Object,
    chartOptions: Object,
    type: {
        type: String,
        default: 'bar',
    }
})
</script>
