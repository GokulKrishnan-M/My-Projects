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
        Schema::create('bookings', function (Blueprint $table) {
            $table->bigIncrements('bookid');
            $table->unsignedBigInteger('custid')->nullable();
            $table->index('custid');
            $table->foreign('custid')->references('custid')->on('customers')->onDelete('cascade');

            $table->unsignedBigInteger('instid')->nullable();
            $table->index('instid');
            $table->foreign('instid')->references('instid')->on('instruments')->onDelete('cascade');

            $table->date('bookdate');
            $table->date('startdate');
            $table->date('returndate');
            $table->integer('quantity');
            $table->integer('totalamt');
            $table->string('status');
            $table->integer('fine')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('bookings');
    }
};
