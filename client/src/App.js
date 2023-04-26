import {
  ChakraProvider,
  Heading,
  Container,
  Text,
  Input,
  Button,
  Wrap,
  Stack,
  Image,
  Spinner,
  Select,
} from "@chakra-ui/react";

import {
  FormControl,
  FormLabel,
  FormErrorMessage,
  FormHelperText,
  FormErrorIcon,
} from "@chakra-ui/form-control"

import {
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
} from '@chakra-ui/react'

import {
  List,
  ListItem,
  ListIcon,
  OrderedList,
  UnorderedList,
} from '@chakra-ui/react'

import { SimpleGrid } from '@chakra-ui/react'

import { Box } from '@chakra-ui/react'

import axios from "axios";
import { useState } from "react";

const App = () => {
  const [image, updateImage] = useState();
  const [prompt, updatePrompt] = useState("");
  const [neg_prompt, updateNegPrompt] = useState("");
  const [selected_model, updateSelectedModel] = useState("runwayml/stable-diffusion-v1-5");
  const [selected_scheduler, updateSelectedScheduler] = useState("PNDMScheduler");
  const [guidance, updateGuidance] = useState(7.5);
  const [seed, updateSeed] = useState(0);
  const [steps, updateSteps] = useState(50);
  const [loading, updateLoading] = useState(false);
  const [error, updateError] = useState(false);
  const [errorMessage, updateErrorMessage] = useState("error");

  const parse = (val) => val.replace(/^\$/, '')

  const checkError = () => {

    var result = false;

    if (!prompt) {
      updateErrorMessage("no prompt defined");
      result = true;
    } else if (!selected_model) {
      updateErrorMessage("no model defined");
      result = true;
    } else if (!selected_scheduler) {
      updateErrorMessage("no scheduler defined");
      result = true;
    } else if (!guidance) {
      updateErrorMessage("no guidance");
      result = true;
    } else if (!steps) {
      updateErrorMessage("no steps");
      result = true;
    } else if (!seed && seed != 0) {
      updateErrorMessage("no seed");
      result = true;
    }
    return result;
  }

  const generate = async (prompt) => {
    if (checkError()) {
      updateError(true);
    } else {
      updateError(false);
      updateLoading(true);
      const config = {
        headers:{
          "ngrok-skip-browser-warning": "69420"
        }
      };
      const result = await axios.get(`https://2fde-2a02-1812-2409-3200-a0a2-e7fd-7c6c-8bb1.ngrok-free.app/generate?prompt=${prompt}&negative_prompt=${neg_prompt}&steps=${steps}&seed=${seed}&guidance=${guidance}&scheduler=${selected_scheduler}&selected_model=${selected_model}&amount=1`,config);
      updateImage(result.data[0]);
      updateLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Container maxW='800px'>
        <Heading>Tool of North America - Stable Diffusion🚀</Heading>

        <Box marginTop={"10px"} marginBottom={"10px"} bg='black' color='white' p={4} borderWidth='1px' borderRadius='lg' >TEXT TO IMAGE</Box>

        <Text>We provide 4 base models and other custom models.</Text>
        <Text marginBottom={"10px"}>When using custom model, include this prefix in the prompt</Text>
        <UnorderedList marginBottom={"30px"}>
         <ListItem>wimvanhenden/ultimate-country: <b>ultmtcntry</b></ListItem>
          <ListItem>nitrosocke/Arcane-Diffusion: <b>arcane style</b></ListItem>
          <ListItem>prompthero/openjourney <b>mdjrny-v4 style</b></ListItem>
        </UnorderedList>


        <Wrap marginBottom={"10px"}>
          <Input placeholder='prompt' value={prompt} onChange={(e) => updatePrompt(e.target.value)}></Input>
          <Text>ugly,duplicate, mutilated, out of frame,  mutation, blurry, bad anatomy, extra legs,low resolution,disfigured</Text>
          <Input placeholder='negative prompt' value={neg_prompt} onChange={(e) => updateNegPrompt(e.target.value)}></Input>

          <FormControl>
            <FormLabel>Model</FormLabel>
            <Select placeholder='runwayml/stable-diffusion-v1-5' value={selected_model} onChange={(e) => updateSelectedModel(e.target.value)} >
              <option>runwayml/stable-diffusion-v1-5</option>
              <option>wimvanhenden/ultimate-country-photo-v1</option>
              <option>wimvanhenden/ultimate-country-photo-v2</option>
              <option>wimvanhenden/ultimate-country-photo-v3</option>
              <option>wimvanhenden/ultimate-country-texture-v1</option>
              <option>wimvanhenden/ultimate-country-texture-v2</option>
              <option>wimvanhenden/ultimate-country-texture-v3</option>           
              <option>nitrosocke/Arcane-Diffusion</option>
              <option>prompthero/openjourney</option>
            </Select>
          </FormControl>

          <FormControl>
            <FormLabel>Scheduler</FormLabel>
            <Select placeholder='PNDMScheduler' value={selected_scheduler} onChange={(e) => updateSelectedScheduler(e.target.value)} >
              <option>PNDMScheduler</option>
              <option>LMSDiscreteScheduler</option>
              <option>DDIMScheduler</option>
              <option>EulerDiscreteScheduler</option>
              <option>EulerAncestralDiscreteScheduler</option>
              <option>DPMSolverMultistepScheduler</option>
            </Select>
          </FormControl>
        </Wrap>
        <SimpleGrid marginBottom={"10px"} columns={3} spacing={0}>
          <Text>Guidance:</Text>
          <Text>Steps:</Text>
          <Text>Seed:</Text>
          <NumberInput value={guidance} precision={2} step={0.1} onChange={(valueString) => updateGuidance(parse(valueString))} ><NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper></NumberInput>
          <NumberInput value={steps} precision={0} step={1} onChange={(valueString) => updateSteps(parse(valueString))} ><NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper></NumberInput>
          <NumberInput value={seed} precision={0} step={1} onChange={(valueString) => updateSeed(parse(valueString))} ><NumberInputField /><NumberInputStepper><NumberIncrementStepper /><NumberDecrementStepper /></NumberInputStepper></NumberInput>
        </SimpleGrid>

        <Button onClick={(e) => generate(prompt)} marginBottom={"10px"} >Generate</Button>

        {error ? (<Box marginTop={"10px"} marginBottom={"10px"} bg='black' color='white' p={4} borderWidth='1px' borderRadius='lg' >ERROR: {errorMessage}</Box>) : null}

        {loading ? (<Stack><Spinner size='xl' /></Stack>) : image ? (<Image src={`${image}`} boxShadow="lg" />) : null}
      </Container>
    </ChakraProvider>
  );
};

export default App;
