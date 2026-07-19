import './App.css';
import Home from './pages/Home'
import Login from './pages/Login';
import Register from './pages/Register';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute'
import PublicRoute from './components/PublicRoute'
import Admin from './pages/Admin'
import Partner from './pages/Partner'


function App() {
  return (
    <Router>
      <Routes>
        <Route path='/home' element={<ProtectedRoute><Home/></ProtectedRoute>}/>
        <Route path='/login' element={<PublicRoute><Login/></PublicRoute>}/>
        <Route path='/register' element={<PublicRoute><Register/></PublicRoute>}/>
        <Route path='/admin' element={<Admin/>}></Route>
        <Route path='/partner' element={<Partner/>}></Route>
      </Routes>
    </Router>
  );
}

export default App;
