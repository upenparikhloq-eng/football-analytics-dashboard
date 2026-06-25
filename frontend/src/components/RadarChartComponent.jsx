import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer
} from "recharts";

function RadarChartComponent({ radarData }) {

  const data = Object.entries(radarData).map(
    ([metric, value]) => ({
      metric,
      value
    })
  );

  return (
    <ResponsiveContainer
      width="100%"
      height={400}
    >
      <RadarChart data={data}>

        <PolarGrid />

        <PolarAngleAxis
          dataKey="metric"
        />

        <PolarRadiusAxis
          domain={[0, 100]}
        />

        <Radar
          name="Player"
          dataKey="value"
          fill="#ffb703"
          fillOpacity={0.6}
        />

      </RadarChart>
    </ResponsiveContainer>
  );
}

export default RadarChartComponent;