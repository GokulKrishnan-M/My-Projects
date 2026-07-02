<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\Subcategory;

class Instrument extends Model
{
    use HasFactory;
    protected $primaryKey='instid';
    protected $fillable=['instname','image','desc','ppd','stock','status','subcatid'];

    public function subcat()
    {
        return $this->belongsTo(Subcategory::class, 'catid', 'catid');
    }
}
