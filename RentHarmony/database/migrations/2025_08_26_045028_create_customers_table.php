<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('customers', function (Blueprint $table) {
            $table->bigIncrements('custid');
            $table->string('custname');
            $table->string('email');
            $table->date('regdate');
            $table->biginteger('contno');
            $table->string('username');
            $table->string('password');
            $table->unsignedBigInteger('locationid')->nullable();
            $table->index('locationid');
            $table->foreign('locationid')->references('locations')->on('locations')->onDelete('cascade');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('customers');
    }
};
