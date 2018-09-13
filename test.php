<?php

// TRAITS
// Mechanism to reuse code in simple inheritance languages
// It reduces the simple inheritance limitations making developers able to reuse at will groups of methods
// over various independent different classes

// A trait is similar to a class but its aim is to group specific functionalities in a coherent way. A trait
// can not be instanced directly
// it allows to combine class members without having to use inheritance


class Base {

    public function sayHello() {
        echo "Hello";
    }

}

trait sayWorld {
    public function sayHello() {
        parent::sayHello();
        echo " World!";
    }
}

class MyHelloWorld extends Base {
    use sayWorld;
}

$obj = new MyHelloWorld();
$obj->sayHello();

echo "<br>*************************************************************<br>";

trait HelloWorld {
    public function sayHello() {
        echo 'Hello';
    }
}

class HelloUniverse {
    use HelloWorld;
    public function sayHello() {
        echo 'Nope Nada';
    }
}

$obj = new HelloUniverse();
$obj->sayHello();

echo "<br>*************************************************************<br>";

trait Hello {
    public function sayHello() {
        echo 'Hello ';
    }
}

trait world {
    public function sayWorld() {
        echo 'World';
    }
}

class MyHWorld {
    use Hello, World;
    public function sayExclamation() {
        echo '!';
    }
}

$obj = new MyHWorld();
$obj->sayHello();
$obj->sayWorld();
$obj->sayExclamation();

echo "<br>*************************************************************<br>";

trait A {
    public function smallTalk() {
        echo 'a';
    }
    public function bigTalk() {
        echo 'A';
    }
}

trait B {
    public function smallTalk() {
        echo 'b';
    }
    public function bigTalk() {
        echo 'B';
    }
}

class Talker {
    use A, B {
        B::smallTalk insteadof A;
        A::bigTalk insteadof B;
        A::bigTalk as talk;
    }
}

$obj = new Talker();
$obj->bigTalk();
$obj->smallTalk();

echo "<br>*************************************************************<br>";

trait Hola {

    public function decirHolaMundo() {
        echo "Holalll " . $this->obtenerMundo();
    }

    public abstract function obtenerMundo();
}

class MiHolaMundo {

    private $mundo;
    use Hola;

    public function obtenerMundo() {
        return $this->mundo;
    }

    public function setMundo($val) {
        $this->mundo = $val;
    }

}

$obj = new MiHolaMundo();
$obj->setMundo("mundooolll");
$obj->decirHolaMundo();

echo "<br>*************************************************************<br>";

trait Contador {


    public function inc() {
        static $c = 0;
        $c = $c + 1;
        echo $c . '<br>';
    }
}

class C1 {
    use Contador;
}

class C2 {
    use Contador;
}

$o1 = new C1;
$o2 = new C2;
$o1->inc();
$o1->inc();
$o2->inc();
$o1->inc();
$o1->inc();
$o2->inc();

echo "<br>*************************************************************<br>";
echo "<br>*************************************************************<br>";
echo "<br>*************************************************************<br>";

/**
 * Closures enable us to create functions not having a name. Anonymous functions.
 * They are useful as a parameter return's value
 */

class CLO {
    private $x = 1;
}
class BLU {
    private $x = 10;
}

$value = function() {
    return $this->x;
};

echo $value->call(new CLO);
echo $value->call(new BLU);

echo "<br>*************************************************************<br>";

$mensaje = ' mensaje';

$ejemplo = function ($arg) use (&$mensaje) {
    $mensaje = " too";
    echo $arg . $mensaje . '<br>';
};

$ejemplo('tu');

echo $mensaje;

echo "<br>*************************************************************<br>";

class HelloWorldQ {
    private $greeting = "Hello";
}

$closure = function($whom) { echo $this->greeting . ' ' . $whom; };

$obj = new HelloWorldQ();
$closure->call($obj, 'World'); // Hello World
