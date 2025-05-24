import { Suspense, lazy } from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"

import { Sidebar } from './components';
import { navItems } from './models/models';
import './App.css';

const Heatmap = lazy(() =>
  import('./components/heatmap/Heatmap')
    .then(module => ({ default: module.Heatmap }))
);


export const App = () => {
  return (
   <BrowserRouter>
      <div className="flex h-screen bg-black text-black-900">
        <div className="w-1/5">
          <Sidebar items={navItems} />
        </div>

        <main className="w-4/5 bg-gray-100 overflow-auto">
          <Suspense fallback={<div className="text-lg font-medium">Cargando…</div>}>
            <Routes>
              <Route path="/" element={<Navigate to="/home" replace />} />
              <Route path="/home" element={<div className="text-xl font-semibold">Home</div>} />
              <Route path="/heatmap" element={<Heatmap />} />
            </Routes>
          </Suspense>
        </main>
      </div>
    </BrowserRouter>
  )
}