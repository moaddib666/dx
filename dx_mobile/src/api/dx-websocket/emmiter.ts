import { Emitter } from "mitt";
import { Events } from "./events";

export interface EventBus extends Emitter<Events> {
    emit<Type extends keyof Events>(type: Type, event?: Events[Type]): void;
    on<Type extends keyof Events>(type: Type, handler: (event: Events[Type]) => void): void;
    off<Type extends keyof Events>(type: Type, handler: (event: Events[Type]) => void): void;
}
