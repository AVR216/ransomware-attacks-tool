import { Suspense, lazy } from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"

import { Sidebar, Modal, CountryInfo, Home, RiskScore } from './components';
import { navItems } from './models/models';
import './App.css';
import { ModalProvider } from "./context/ModalContext";


const Heatmap = lazy(() =>
  import('./components/heatmap/Heatmap')
    .then(module => ({ default: module.Heatmap }))
);


export const App = () => {
  return (
    <ModalProvider>
      <BrowserRouter>
        <div className="flex h-screen bg-black text-black-900">
          <div className="w-1/5">
            <Sidebar items={navItems} />
          </div>

          <main className="w-4/5 bg-gray-100 overflow-auto">
            <Suspense fallback={<div className="text-lg font-medium">Cargando…</div>}>
              <Routes>
                <Route path="/" element={<Navigate to="/home" replace />} />
                <Route path="/home" element={ <Home /> } />
                <Route path="/heatmap" element={<Heatmap />} />
                <Route path="/dangerous-groups" element={ <RiskScore /> } />
              </Routes>
            </Suspense>
          </main>
        </div>
      </BrowserRouter>
      <Modal>
        <CountryInfo />
      </Modal>
    </ModalProvider>
     )
}