import React, { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useQuery } from 'react-query'
import axios from 'axios'

interface ForecastChartProps {
  latitude: number
  longitude: number
}

interface ForecastData {
  timestamp: string
  pm25: number
  o3: number
  no2: number
  aqi: number
}

const ForecastChart: React.FC<ForecastChartProps> = ({ latitude, longitude }) => {
  const [forecastHours, setForecastHours] = useState(24)

  const { data: forecastData, isLoading, error } = useQuery(
    ['forecast', latitude, longitude, forecastHours],
    async () => {
      const response = await axios.post('/api/v1/forecast', {
        latitude,
        longitude,
        forecast_hours: forecastHours,
        include_confidence: true
      })
      return response.data
    },
    {
      enabled: !!latitude && !!longitude,
      refetchInterval: 300000, // Refetch every 5 minutes
    }
  )

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getAQIColor = (aqi: number) => {
    if (aqi <= 50) return '#00e400'
    if (aqi <= 100) return '#ffff00'
    if (aqi <= 150) return '#ff7e00'
    if (aqi <= 200) return '#ff0000'
    if (aqi <= 300) return '#8f3f97'
    return '#7e0023'
  }

  const getAQILabel = (aqi: number) => {
    if (aqi <= 50) return 'Good'
    if (aqi <= 100) return 'Moderate'
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups'
    if (aqi <= 200) return 'Unhealthy'
    if (aqi <= 300) return 'Very Unhealthy'
    return 'Hazardous'
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2 text-gray-600">Loading forecast...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8 text-red-600">
        <p>Error loading forecast data</p>
        <p className="text-sm text-gray-500 mt-1">Please try again later</p>
      </div>
    )
  }

  const chartData = forecastData?.forecast_data?.map((point: any) => ({
    timestamp: formatTime(point.timestamp),
    pm25: point.pm25?.toFixed(1) || 0,
    o3: point.o3?.toFixed(1) || 0,
    no2: point.no2?.toFixed(1) || 0,
    aqi: point.aqi || 0,
    fullTimestamp: point.timestamp
  })) || []

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium text-gray-700">Forecast Period:</label>
          <select
            value={forecastHours}
            onChange={(e) => setForecastHours(Number(e.target.value))}
            className="border border-gray-300 rounded-md px-3 py-1 text-sm"
          >
            <option value={24}>24 Hours</option>
            <option value={48}>48 Hours</option>
            <option value={72}>72 Hours</option>
          </select>
        </div>
        
        <div className="text-sm text-gray-500">
          Last updated: {forecastData?.generated_at ? new Date(forecastData.generated_at).toLocaleString() : 'Unknown'}
        </div>
      </div>

      {/* Current AQI Display */}
      {chartData.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Current Air Quality</h3>
              <p className="text-sm text-gray-600">Based on latest forecast</p>
            </div>
            <div className="text-right">
              <div 
                className="text-3xl font-bold"
                style={{ color: getAQIColor(chartData[0].aqi) }}
              >
                {chartData[0].aqi}
              </div>
              <div 
                className="text-sm font-medium"
                style={{ color: getAQIColor(chartData[0].aqi) }}
              >
                {getAQILabel(chartData[0].aqi)}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Chart */}
      <div className="bg-white rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Air Quality Forecast</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="timestamp" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis 
              yAxisId="pollutants"
              orientation="left"
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              yAxisId="aqi"
              orientation="right"
              domain={[0, 300]}
              tick={{ fontSize: 12 }}
            />
            <Tooltip 
              formatter={(value: any, name: string) => [
                `${value}${name === 'aqi' ? '' : name === 'pm25' ? ' μg/m³' : ' ppb'}`,
                name.toUpperCase()
              ]}
              labelFormatter={(label) => `Time: ${label}`}
            />
            <Legend />
            <Line
              yAxisId="pollutants"
              type="monotone"
              dataKey="pm25"
              stroke="#8884d8"
              strokeWidth={2}
              name="PM2.5"
              dot={false}
            />
            <Line
              yAxisId="pollutants"
              type="monotone"
              dataKey="o3"
              stroke="#82ca9d"
              strokeWidth={2}
              name="O3"
              dot={false}
            />
            <Line
              yAxisId="pollutants"
              type="monotone"
              dataKey="no2"
              stroke="#ffc658"
              strokeWidth={2}
              name="NO2"
              dot={false}
            />
            <Line
              yAxisId="aqi"
              type="monotone"
              dataKey="aqi"
              stroke="#ff7300"
              strokeWidth={3}
              name="AQI"
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Data Source Info */}
      <div className="bg-blue-50 rounded-lg p-4">
        <h4 className="text-sm font-medium text-blue-900 mb-2">Data Sources</h4>
        <div className="text-sm text-blue-800">
          <p>• NASA TEMPO satellite observations</p>
          <p>• AirNow ground monitoring stations</p>
          <p>• NOAA weather forecasts</p>
          <p>• Machine learning fusion models</p>
        </div>
      </div>
    </div>
  )
}

export default ForecastChart
