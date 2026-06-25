import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Legend,
  ResponsiveContainer
} from "recharts";

function CompareRadarChart({ comparisonData }) {

  const player1 =
    comparisonData.player1;

  const player2 =
    comparisonData.player2;

  const categories = Object.keys(
    player1.stats
  );

  const chartData = categories.map(
    (category) => ({
      metric: category,
      [player1.name]:
        player1.stats[category],
      [player2.name]:
        player2.stats[category]
    })
  );

  return (

    <ResponsiveContainer
      width="100%"
      height={500}
    >

      <RadarChart
        data={chartData}
      >

        <PolarGrid />

        <PolarAngleAxis
          dataKey="metric"
        />

        <PolarRadiusAxis
          domain={[0, 100]}
        />

        <Radar
          name={player1.name}
          dataKey={player1.name}
          stroke="#6CB4EE"
          fill="#6CB4EE"
          fillOpacity={0.3}
        />

        <Radar
          name={player2.name}
          dataKey={player2.name}
          stroke="#ff4d4d"
          fill="#ff4d4d"
          fillOpacity={0.3}
        />

        <Legend />

      </RadarChart>

    </ResponsiveContainer>

  );

}

export default CompareRadarChart;