import { Routes } from '@angular/router';

import { RegisterComponent } from './features/auth/pages/register/register.component';
import { LoginComponent } from './features/auth/pages/login/login.component';
import { InventoryComponent } from './inventory/component/inventory.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
    {path: '', component:LoginComponent},
    {path:'register', component:RegisterComponent},
    {path:'login', component:LoginComponent},
    {path:'inventory', component:InventoryComponent, canActivate:[AuthGuard]},
    {path: '**', redirectTo: '' }
];
