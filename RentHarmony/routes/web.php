<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AdminController;
use App\Http\Controllers\DistrictController;
use App\Http\Controllers\GuestController;
use App\Http\Controllers\LoginController;
use App\Http\Controllers\LocationController;
use App\Http\Controllers\CategoryController;
use App\Http\Controllers\SubcategoryController;
use App\Http\Controllers\InstrumentController;
use App\Http\Controllers\CustomerController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/viewindex',[AdminController::class, 'index'])->name('index');
Route::get('',[GuestController::class, 'guestview'])->name('guestview');
Route::get('/districtview',[DistrictController::class, 'district'])->name('district');
Route::get('/adminlogin',[LoginController::class, 'adminlogin'])->name('adminlogin');
Route::post('/adminloginp',[LoginController::class, 'adminlogin_process'])->name('adminlogin_process');
Route::post('/distinsert',[DistrictController::class, 'district_insert'])->name('district_insert');
Route::get('/districttable',[DistrictController::class, 'viewdistrict'])->name('viewdistrict');
Route::get('deletedist/{districtid}',[DistrictController::class, 'deletedist'])->name('deletedist');
Route::get('updatedist/{districtid}',[DistrictController::class, 'updatedist'])->name('updatedist');
Route::post('/updatedisttable{dist}',[DistrictController::class, 'updatedisttable'])->name('updatedisttable');
Route::get('/location',[LocationController::class, 'location'])->name('location');
Route::post('/locationinsert',[LocationController::class, 'location_insert'])->name('location_insert');
Route::get('/locationview',[LocationController::class, 'location_view'])->name('location_view');
Route::get('/getloc/{districtid}',[LocationController::class, 'getloc'])->name('getloc');
Route::get('deleteloc/{locationid}',[LocationController::class, 'deleteloc'])->name('deleteloc');
Route::get('updateloc/{locationid}',[LocationController::class, 'updateloc'])->name('updateloc');
Route::post('/updateloctable{loc}',[LocationController::class, 'updateloctable'])->name('updateloctable');
Route::get('/category',[CategoryController::class, 'category'])->name('category');
Route::post('/categoryinsert',[CategoryController::class, 'categoryinsert'])->name('categoryinsert');
Route::get('/categoryview',[CategoryController::class, 'categoryview'])->name('categoryview');
Route::get('deletecat/{catid}',[CategoryController::class, 'deletecat'])->name('deletecat');
Route::get('updatecat/{catid}',[CategoryController::class, 'updatecat'])->name('updatecat');
Route::post('/update_cat{cat}',[CategoryController::class, 'update_cat'])->name('update_cat');
Route::get('/subcategory',[SubcategoryController::class, 'subcategory'])->name('subcategory');
Route::post('/subcatinsert',[SubcategoryController::class, 'subcatinsert'])->name('subcatinsert');
Route::get('/subcatview',[SubcategoryController::class, 'subcatview'])->name('subcatview');
Route::get('getsubcat/{catid}',[SubcategoryController::class, 'getsubcat'])->name('getsubcat');
Route::get('deletesubcat/{subcatid}',[SubcategoryController::class, 'deletesubcat'])->name('deletesubcat');
Route::get('updatesubcat/{subcatid}',[SubcategoryController::class, 'updatesubcat'])->name('updatesubcat');
Route::post('/update_subcat/{subcat}',[SubcategoryController::class, 'update_subcat'])->name('update_subcat');
Route::get('/instrument',[InstrumentController::class, 'instrument'])->name('instrument');
Route::get('getsubcatid/{catid}',[InstrumentController::class, 'getsubcatid'])->name('getsubcatid');
Route::post('/instinsert',[InstrumentController::class, 'instinsert'])->name('instinsert');
Route::get('/instview',[InstrumentController::class, 'instview'])->name('instview');
Route::get('/getinst/{subcatid}',[InstrumentController::class, 'getinst'])->name('getinst');
Route::get('deleteinst/{instid}',[InstrumentController::class, 'deleteinst'])->name('deleteinst');
Route::get('updateinst/{instid}',[InstrumentController::class, 'updateinst'])->name('updateinst');
Route::post('/update_inst/{instid}',[InstrumentController::class, 'update_inst'])->name('update_inst');
Route::get('/customerreg',[CustomerController::class, 'customer'])->name('customer');
Route::get('/getloc/{districtid}',[CustomerController::class, 'getloc'])->name('getloc');
Route::post('custinsert',[CustomerController::class, 'custinsert'])->name('custinsert');
Route::get('/customerhome',[CustomerController::class, 'customerhome'])->name('customerhome');
Route::get('/customerlogin',[GuestController::class, 'customerlogin'])->name('customerlogin');
Route::post('/customerlogin_process',[GuestController::class, 'customerlogin_process'])->name('customerlogin_process');
Route::get('/customercatview',[CustomerController::class, 'customercatview'])->name('customercatview');
Route::get('/customersubcatview/{catid}',[CustomerController::class, 'subcategoryview'])->name('customersubcatview');
Route::get('/customerinstview/{subcatid}',[CustomerController::class, 'Instview'])->name('customerinstview');
Route::get('instrumentsingle{instid}',[CustomerController::class, 'instrumentsingle'])->name('instsingle');
Route::get('booking/{instid}',[CustomerController::class, 'booking'])->name('booking');
Route::post('booking_payment_insert/',[CustomerController::class, 'booking_payment_insert'])->name('booking_payment_insert');
Route::get('customerview',[CustomerController::class, 'customerview'])->name('customerview');
Route::get('shop',[CustomerController::class, 'shop'])->name('shop');
Route::get('viewmorebook/{bookid}',[CustomerController::class, 'viewmorebook'])->name('viewmorebook');
Route::post('returnBooking/{bookid}',[CustomerController::class, 'returnBooking'])->name('returnBooking');
Route::get('profile',[CustomerController::class, 'profile'])->name('profile');
