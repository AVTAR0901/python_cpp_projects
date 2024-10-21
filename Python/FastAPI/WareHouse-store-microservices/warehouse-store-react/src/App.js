import './App.css';
import {Routes, Route, BrowserRouter} from 'react-router-dom';
import { Products } from './routes/Products';
import { ProductsCreate } from './routes/ProductCreate';
import { Order } from './routes/Order';

function App() {
  //Routes here are linked to frontend pages in Products.js
  return (
  <BrowserRouter>
  <Routes>
  <Route path="/" element={<Products/>}/>
  <Route path='/create' element={<ProductsCreate/>}/>
  <Route path='/order' element={<Order/>}/>
  </Routes>
  </BrowserRouter>
  );
}

export default App;
