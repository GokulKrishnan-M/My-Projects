<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\District;

class Location extends Model
{
    use HasFactory;

    protected $primaryKey='locationid';
    protected $fillable=['locationname','districtid'];

    public function dist()
    {
        return $this->belongsTo(District::class, 'districtid', 'districtid');
    }
}
