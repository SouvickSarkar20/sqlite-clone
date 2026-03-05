import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Editor from './pages/Editor';

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ maxWidth: '100%', margin: '0', padding: '2rem 5vw', width: '100%' }}>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/editor" element={<Editor />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
