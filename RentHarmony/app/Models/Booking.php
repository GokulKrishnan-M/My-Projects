<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Booking extends Model
{
    use HasFactory;
     protected $primaryKey='bookid';
    protected $fillable=['custid','instid','bookdate','startdate','returndate','quantity','totalamt','status','fine'];

    public function cust()
    {
        return $this->belongsTo(Customer::class, 'custid', 'custid');
    }
    public function inst()
    {
        return $this->belongsTo(Instrument::class, 'instid', 'instid');
    }
}
