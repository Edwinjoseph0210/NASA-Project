import React, { useState } from 'react'
import { useQuery } from 'react-query'
import axios from 'axios'
import { MapPin, Activity, Clock, AlertCircle } from 'lucide-react'

interface Station {
  id: string
  station_id: string
  name: string
  latitude: number
  longitude: number
  state: string
  city: string
  is_active: boolean
}

interface StationReading {
  timestamp: string
  pm25: number
  o3: number
  no2: number
  overall_aqi: number
  quality_flag: string
  data_source: string
}

const StationList: React.FC = () => {
  const [selectedStation, setSelectedStation] = useState<Station | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedState, setSelectedState] = useState('')

  const { data: stationsData, isLoading: stationsLoading } = useQuery(
    ['stations', selectedState],
    async () => {
      const params = new URLSearchParams()
      if (selectedState) params.append('state', selectedState)
      if (searchTerm) params.append('search', searchTerm)
      
      const response = await axios.get(`/api/v1/stations?${params}`)
      return response.data
    },
    {
      refetchInterval: 300000, // Refetch every 5 minutes
    }
  )

  const { data: readingsData, isLoading: readingsLoading } = useQuery(
    ['station-readings', selectedStation?.station_id],
    async () => {
      if (!selectedStation) return null
      
      const response = await axios.get(
        `/api/v1/stations/${selectedStation.station_id}/readings?hours=24`
      )
      return response.data
    },
    {
      enabled: !!selectedStation,
      refetchInterval: 60000, // Refetch every minute
    }
  )

  const getAQIColor = (aqi: number) => {
    if (aqi <= 50) return 'text-green-600 bg-green-100'
    if (aqi <= 100) return 'text-yellow-600 bg-yellow-100'
    if (aqi <= 150) return 'text-orange-600 bg-orange-100'
    if (aqi <= 200) return 'text-red-600 bg-red-100'
    if (aqi <= 300) return 'text-purple-600 bg-purple-100'
    return 'text-red-800 bg-red-200'
  }

  const getAQILabel = (aqi: number) => {
    if (aqi <= 50) return 'Good'
    if (aqi <= 100) return 'Moderate'
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups'
    if (aqi <= 200) return 'Unhealthy'
    if (aqi <= 300) return 'Very Unhealthy'
    return 'Hazardous'
  }

  const stations = stationsData?.stations || []
  const readings = readingsData?.readings || []

  // Get unique states for filter
  const states = Array.from(new Set(stations.map((s: Station) => s.state))).sort()

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search stations..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All States</option>
            {states.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Stations List */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <h3 className="text-lg font-semibold text-gray-900">
              Monitoring Stations ({stations.length})
            </h3>
          </div>
          
          <div className="max-h-96 overflow-y-auto">
            {stationsLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                <span className="ml-2 text-gray-600">Loading stations...</span>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {stations.map((station: Station) => (
                  <div
                    key={station.id}
                    onClick={() => setSelectedStation(station)}
                    className={`p-4 cursor-pointer hover:bg-gray-50 ${
                      selectedStation?.id === station.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="text-sm font-medium text-gray-900">
                          {station.name}
                        </h4>
                        <p className="text-sm text-gray-600">
                          {station.city}, {station.state}
                        </p>
                        <div className="flex items-center mt-1 text-xs text-gray-500">
                          <MapPin className="h-3 w-3 mr-1" />
                          {station.latitude.toFixed(4)}, {station.longitude.toFixed(4)}
                        </div>
                      </div>
                      <div className="flex items-center">
                        <div className={`px-2 py-1 rounded-full text-xs ${
                          station.is_active 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {station.is_active ? 'Active' : 'Inactive'}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Station Details */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <h3 className="text-lg font-semibold text-gray-900">
              Station Details
            </h3>
          </div>
          
          <div className="p-6">
            {selectedStation ? (
              <div className="space-y-6">
                {/* Station Info */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Station Information</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Name:</span>
                      <span className="font-medium">{selectedStation.name}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">ID:</span>
                      <span className="font-medium">{selectedStation.station_id}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Location:</span>
                      <span className="font-medium">{selectedStation.city}, {selectedStation.state}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Coordinates:</span>
                      <span className="font-medium">
                        {selectedStation.latitude.toFixed(4)}, {selectedStation.longitude.toFixed(4)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Status:</span>
                      <span className={`font-medium ${
                        selectedStation.is_active ? 'text-green-600' : 'text-gray-600'
                      }`}>
                        {selectedStation.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Latest Readings */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Latest Readings</h4>
                  {readingsLoading ? (
                    <div className="flex items-center justify-center py-4">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                      <span className="ml-2 text-gray-600 text-sm">Loading readings...</span>
                    </div>
                  ) : readings.length > 0 ? (
                    <div className="space-y-3">
                      {readings.slice(0, 3).map((reading: StationReading, index: number) => (
                        <div key={index} className="bg-gray-50 rounded-lg p-3">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center text-sm text-gray-600">
                              <Clock className="h-3 w-3 mr-1" />
                              {new Date(reading.timestamp).toLocaleString()}
                            </div>
                            <div className={`px-2 py-1 rounded-full text-xs font-medium ${getAQIColor(reading.overall_aqi)}`}>
                              {getAQILabel(reading.overall_aqi)}
                            </div>
                          </div>
                          <div className="grid grid-cols-2 gap-2 text-sm">
                            <div className="flex justify-between">
                              <span className="text-gray-600">PM2.5:</span>
                              <span className="font-medium">{reading.pm25?.toFixed(1) || 'N/A'} μg/m³</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-600">O3:</span>
                              <span className="font-medium">{reading.o3?.toFixed(1) || 'N/A'} ppb</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-600">NO2:</span>
                              <span className="font-medium">{reading.no2?.toFixed(1) || 'N/A'} ppb</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-600">AQI:</span>
                              <span className="font-medium">{reading.overall_aqi || 'N/A'}</span>
                            </div>
                          </div>
                          <div className="mt-2 text-xs text-gray-500">
                            Source: {reading.data_source}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-4 text-gray-500">
                      <AlertCircle className="h-8 w-8 mx-auto mb-2 text-gray-400" />
                      <p className="text-sm">No recent readings available</p>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Activity className="h-8 w-8 mx-auto mb-2 text-gray-400" />
                <p className="text-sm">Select a station to view details</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default StationList
