import React, { useState, useEffect } from 'react'
import Head from 'next/head'
import dynamic from 'next/dynamic'

// Dynamically import map component
const KeralaMap = dynamic(() => import('../components/KeralaMap'), {
  ssr: false,
  loading: () => <div className="flex items-center justify-center h-96 bg-gray-100 rounded-lg">Loading Kerala map...</div>
})

const KeralaForecast = dynamic(() => import('../components/KeralaForecast'), {
  ssr: false
})

const KeralaStations = dynamic(() => import('../components/KeralaStations'), {
  ssr: false
})

const KeralaAlerts = dynamic(() => import('../components/KeralaAlerts'), {
  ssr: false
})

const KeralaHome: React.FC = () => {
  const [selectedLocation, setSelectedLocation] = useState<{
    latitude: number
    longitude: number
    name?: string
  } | null>(null)

  const [activeTab, setActiveTab] = useState<'map' | 'forecast' | 'stations' | 'alerts'>('map')

  // Default to Kottayam center
  const kottayamCenter = { latitude: 9.5956, longitude: 76.5214, name: 'Kottayam' }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <Head>
        <title>AirAware Kerala - Air Quality Monitoring for Kottayam</title>
        <meta name="description" content="Real-time air quality monitoring and forecasting for Kottayam, Kerala" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-green-800">🌬️ AirAware Kerala</h1>
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Air Quality Monitoring for Kottayam, Kerala</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                🏛️ Powered by NASA TEMPO
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
              { id: 'map', label: 'Kerala Map', icon: '🗺️' },
              { id: 'forecast', label: 'Forecast', icon: '📊' },
              { id: 'stations', label: 'Stations', icon: '📍' },
              { id: 'alerts', label: 'Alerts', icon: '🔔' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-green-500 text-green-600'
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
              <h2 className="text-lg font-semibold text-gray-900 mb-4">🌴 Kerala Air Quality Map</h2>
              <KeralaMap 
                onLocationSelect={setSelectedLocation}
                selectedLocation={selectedLocation || kottayamCenter}
                center={kottayamCenter}
              />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Conditions</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">PM2.5:</span>
                    <span className="font-medium text-green-600">18.2 μg/m³</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">O3:</span>
                    <span className="font-medium text-green-600">42.1 ppb</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">NO2:</span>
                    <span className="font-medium text-green-600">22.7 ppb</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">AQI:</span>
                    <span className="font-medium text-green-600">Good (48)</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Location Info</h3>
                <div className="space-y-2">
                  <p><strong>Location:</strong> {(selectedLocation || kottayamCenter).name}</p>
                  <p><strong>Latitude:</strong> {(selectedLocation || kottayamCenter).latitude.toFixed(4)}</p>
                  <p><strong>Longitude:</strong> {(selectedLocation || kottayamCenter).longitude.toFixed(4)}</p>
                  <p><strong>State:</strong> Kerala, India</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'forecast' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">📊 Kerala Air Quality Forecast</h2>
              <KeralaForecast 
                latitude={(selectedLocation || kottayamCenter).latitude}
                longitude={(selectedLocation || kottayamCenter).longitude}
              />
            </div>
          </div>
        )}

        {activeTab === 'stations' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">📍 Kerala Monitoring Stations</h2>
              <KeralaStations />
            </div>
          </div>
        )}

        {activeTab === 'alerts' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">🔔 Kerala Air Quality Alerts</h2>
              <KeralaAlerts />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>© 2024 AirAware Kerala. Data provided by NASA TEMPO, AirNow, and Kerala State Pollution Control Board.</p>
            <p className="mt-2">
              <a href="/api/docs" className="text-green-600 hover:text-green-800">API Documentation</a>
              {' • '}
              <a href="/about" className="text-green-600 hover:text-green-800">About</a>
              {' • '}
              <a href="/contact" className="text-green-600 hover:text-green-800">Contact</a>
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default KeralaHome
