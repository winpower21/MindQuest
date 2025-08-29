<template>
    <div class="p-4">
        <h1 class="text-2xl font-bold mb-4">Admin Statistics Dashboard</h1>
        <div>
            <button @click="goBack" class="btn btn-dark" style="font-size: larger; margin: 0px 10px 10px 0px;"><i
                    class="bi bi-skip-backward-fill"></i> Back</button>
        </div>
        <div v-if="stats?.totals?.users > 0 && stats?.totals?.quizzes > 0" class="space-y-8">
            <!-- User Performance -->
            <section>
                <h2 class="text-xl font-semibold mb-2">User Performance</h2>
                <div class="row row-cols-2">
                    <div class="col">
                        <ChartCard v-if="stats.avg_score_per_quiz.length" title="Average Score per Quiz"
                            :chart-data="formatChartData(stats.avg_score_per_quiz)" />
                    </div>
                    <div class="col">
                        <ChartCard v-if="stats.top_users.length" title="Top Performing Users"
                            :chart-data="formatChartData(stats.top_users)" />
                    </div>
                    <div class="col">
                        <ChartCard v-if="stats.low_performing_quizzes.length" title="Low Performing Quizzes"
                            :chart-data="formatChartData(stats.low_performing_quizzes)" />
                    </div>
                    <div class="col">
                        <ChartCard v-if="stats.subject_performance.length" title="Performance by Subject"
                            :chart-data="formatChartData(stats.subject_performance)" />
                    </div>
                </div>
            </section>

            <!-- User Activity -->
            <section>
                <h2 class="text-xl font-semibold mb-2">User Activity</h2>

                <div class="row row-cols-2">
                    <div class="col">
                        <ChartCard v-if="stats.daily_active.length" title="Daily Active Users"
                            :chart-data="formatTimeSeries(stats.daily_active, 'date', 'users')" type="line" />
                    </div>
                    <div class="col">
                        <ChartCard v-if="stats.most_active_users.length" title="Most Active Users"
                            :chart-data="formatChartData(stats.most_active_users)" />
                    </div>
                </div>
                <ChartCard v-if="stats.attempt_heatmap.length" title="Attempts by Hour"
                    :chart-data="formatChartData(stats.attempt_heatmap, 'hour', 'count')" />
            </section>

            <!-- Quiz Engagement -->
            <section>
                <h2 class="text-xl font-semibold mb-2">Quiz Engagement</h2>
                <div class="row row-cols-2">
                    <div class="col">
                        <ChartCard v-if="stats.most_attempted_quizzes.length" title="Most Attempted Quizzes"
                            :chart-data="formatChartData(stats.most_attempted_quizzes)" />
                    </div>
                    <div class="col">
                        <ChartCard v-if="stats.avg_attempts_per_quiz.length" title="Average Attempts per Quiz"
                            :chart-data="formatChartData(stats.avg_attempts_per_quiz)" />
                    </div>
                    <div class="col">
                        <ChartCard v-if="stats.completion_rate.length" title="Quiz Completion Rate"
                            :chart-data="formatChartData(stats.completion_rate)" />
                    </div>
                </div>
            </section>

            <!-- Other Insights -->
            <section>
                <h2 class="text-xl font-semibold mb-2">Other Insights</h2>
                <ChartCard v-if="stats.user_growth.length" title="User Growth Over Time"
                    :chart-data="formatTimeSeries(stats.user_growth, 'date', 'count')" type="line" />
                <TableCard v-if="stats.totals" title="Overall Totals" :data="[
                    { label: 'Total Users', value: stats.totals.users },
                    { label: 'Total Quizzes', value: stats.totals.quizzes },
                    { label: 'Total Attempts', value: stats.totals.attempts }
                ]" />
            </section>
        </div>

        <div v-else class="text-center text-gray-500 mt-10">
            <h1>No statistics available yet. Data will appear once users and quizzes are active.</h1>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChartCard from '@/components/ChartCard.vue'
import TableCard from '@/components/TableCard.vue'
import fetchWithAuth from '@/utils/api'
import { useRouter } from 'vue-router'
const router = useRouter();
const stats = ref(null)

onMounted(async () => {
    try {
        const response = await fetchWithAuth('/api/admin/stats')
        stats.value = await response.json()
    } catch (error) {
        console.error('Failed to fetch admin stats:', error)
    }
})

function formatChartData(data, labelKey = 'label', valueKey = 'value') {
    return {
        labels: data.map(d => d[labelKey]),
        datasets: [
            {
                label: 'Value',
                backgroundColor: '#3B82F6',
                data: data.map(d => d[valueKey])
            }
        ]
    }
}

function formatTimeSeries(data, labelKey, valueKey) {
    return {
        labels: data.map(d => d[labelKey]),
        datasets: [
            {
                label: 'Value',
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
                borderColor: '#3B82F6',
                fill: false,
                data: data.map(d => d[valueKey])
            }
        ]
    }
}

function getAxisOptions(xLabel, yLabel) {
    return {
        responsive: true,
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: false
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: xLabel
                }
            },
            y: {
                title: {
                    display: true,
                    text: yLabel
                },
                beginAtZero: true
            }
        }
    }
}

// ============================================================================================================================================
const goBack = () => {
    router.go(-1);  // Goes back one step in history
};
// ============================================================================================================================================

</script>

<style scoped>
section {
    margin-bottom: 2rem;
}
</style>
