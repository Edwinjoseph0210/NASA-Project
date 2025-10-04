import { NextPage } from 'next'
import Head from 'next/head'
import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import { QueryClient, QueryClientProvider } from 'react-query'
import { Toaster } from 'react-hot-toast'

// Dynamically import map component to avoid SSR issues
const AirQualityMap = dynamic(() => import('../components/AirQualityMap'), {
  ssr: false,
  loading: () => <div className="flex items-center justify-center h-96 bg-gray-100 rounded-lg">Loading map...</div>
})

const ForecastChart = dynamic(() => import('../components/ForecastChart'), {
  ssr: false
})

const StationList = dynamic(() => import('../components/StationList'), {
  ssr: false
})

const AlertPanel = dynamic(() => import('../components/AlertPanel'), {
  ssr: false
})

// Create a client
const queryClient = new QueryClient()

const Home: NextPage = () => {
  const [selectedLocation, setSelectedLocation] = useState<{
    latitude: number
    longitude: number
    name?: string
  } | null>(null)

  const [activeTab, setActiveTab] = useState<'map' | 'forecast' | 'stations' | 'alerts'>('map')

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-50">
        <Head>
          <title>AirAware - Real-Time Air Quality Forecasting</title>
          <meta name="description" content="Real-time air quality forecasting using NASA TEMPO satellite data" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <h1 className="text-2xl font-bold text-gray-900">AirAware</h1>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Real-Time Air Quality Forecasting</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-500">
                  Powered by NASA TEMPO
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Navigation Tabs */}
        <nav className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex space-x-8">
              {[
                { id: 'map', label: 'Map', icon: '🗺️' },
                { id: 'forecast', label: 'Forecast', icon: '📊' },
                { id: 'stations', label: 'Stations', icon: '📍' },
                { id: 'alerts', label: 'Alerts', icon: '🔔' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {activeTab === 'map' && (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Air Quality Map</h2>
                <AirQualityMap 
                  onLocationSelect={setSelectedLocation}
                  selectedLocation={selectedLocation}
                />
              </div>
              
              {selectedLocation && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Conditions</h3>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-600">PM2.5:</span>
                        <span className="font-medium">15.2 μg/m³</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">O3:</span>
                        <span className="font-medium">42.1 ppb</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">NO2:</span>
                        <span className="font-medium">18.7 ppb</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">AQI:</span>
                        <span className="font-medium text-green-600">Good (52)</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Location Info</h3>
                    <div className="space-y-2">
                      <p><strong>Latitude:</strong> {selectedLocation.latitude.toFixed(4)}</p>
                      <p><strong>Longitude:</strong> {selectedLocation.longitude.toFixed(4)}</p>
                      {selectedLocation.name && (
                        <p><strong>Location:</strong> {selectedLocation.name}</p>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'forecast' && (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Air Quality Forecast</h2>
                {selectedLocation ? (
                  <ForecastChart 
                    latitude={selectedLocation.latitude}
                    longitude={selectedLocation.longitude}
                  />
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <p>Select a location on the map to view air quality forecast</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'stations' && (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Monitoring Stations</h2>
                <StationList />
              </div>
            </div>
          )}

          {activeTab === 'alerts' && (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Air Quality Alerts</h2>
                <AlertPanel />
              </div>
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="bg-white border-t mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center text-gray-500 text-sm">
              <p>© 2024 AirAware. Data provided by NASA TEMPO, AirNow, and NOAA.</p>
              <p className="mt-2">
                <a href="/api/docs" className="text-blue-600 hover:text-blue-800">API Documentation</a>
                {' • '}
                <a href="/about" className="text-blue-600 hover:text-blue-800">About</a>
                {' • '}
                <a href="/privacy" className="text-blue-600 hover:text-blue-800">Privacy Policy</a>
              </p>
            </div>
          </div>
        </footer>

        <Toaster position="top-right" />
      </div>
    </QueryClientProvider>
  )
}

export default Home
