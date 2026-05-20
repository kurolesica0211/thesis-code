================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Princess Charlotte of Wales (Charlotte Elizabeth Diana; born 2 May 2015) is a member of the British royal family.
She is the second child and only daughter of William, Prince of Wales, and Catherine, Princess of Wales, and a granddaughter of King Charles III and Diana, Princess of Wales.
Infancy

Charlotte was born at 8:34 am on 2 May 2015 at St Mary's Hospital, London, during the reign of her paternal great-grandmother, Queen Elizabeth II.
She is the second child and only daughter of Prince William and Catherine (then known as Duke and Duchess of Cambridge).
She has an older and younger brother, Prince George and Prince Louis.
On 4 May her name was announced as Charlotte Elizabeth Diana, honouring her grandfather Charles, her great-grandmother, and her grandmother Diana.
Charlotte was christened on 5 July by the archbishop of Canterbury, Justin Welby, at St Mary Magdalene Church, Sandringham.
Upbringing

The family lived at Anmer Hall in Norfolk during Charlotte's infancy, before relocating to Kensington Palace in 2017.
Charlotte started at Willcocks Nursery School in January 2018.
She joined George at Thomas's School in Battersea in September 2019, where she was known as Charlotte Cambridge.
In 2022, the family relocated to Adelaide Cottage in Windsor Home Park, after which she and her brothers began attending Lambrook, an independent preparatory school in Berkshire.
Following the death of Elizabeth II on 8 September 2022, Charlotte's grandfather acceded to the throne as Charles III, and Charlotte became third in line to the throne.
Public image

Despite the efforts of her parents to keep their children from public view, photographs and public appearances of Charlotte continue to attract media attention.
Shopping statistics and polls among parents show that Charlotte is a major children's style icon.
Title and styles

Charlotte is a British princess with the official style and title "Her Royal Highness Princess Charlotte of Wales".
Before her father was created Prince of Wales on 9 September 2022, Charlotte was styled "Her Royal Highness Princess Charlotte of Cambridge".
Succession

Charlotte is third in the line of succession to the British throne, behind her father and elder brother.
Because of the implementation of the Perth Agreement, which replaced male-preference primogeniture with absolute primogeniture, she did not move down the line of succession upon the birth of her younger brother Louis in April 2018, making her the first British princess in history to rank above a brother in the line of succession.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (2abf9dc6-706b-4825-9ed4-eff8c970a01f)
 Call ID: 2abf9dc6-706b-4825-9ed4-eff8c970a01f
  Args:
    type: :Person
    source: Charlotte_of_Wales
  AssignClass (202666f3-0e58-4269-88f4-54b89d019fbe)
 Call ID: 202666f3-0e58-4269-88f4-54b89d019fbe
  Args:
    type: :Woman
    source: Charlotte_of_Wales
  AssignClass (cc9aa674-9dc3-4500-9a69-ff2c2d0953e9)
 Call ID: cc9aa674-9dc3-4500-9a69-ff2c2d0953e9
  Args:
    source: William_Prince_of_Wales
    type: :Person
  AssignClass (ecb847ca-3644-430d-a158-66d09cc32b9e)
 Call ID: ecb847ca-3644-430d-a158-66d09cc32b9e
  Args:
    source: William_Prince_of_Wales
    type: :Man
  AssignClass (b68ba882-5742-4bae-9cfb-b6eb6aad665e)
 Call ID: b68ba882-5742-4bae-9cfb-b6eb6aad665e
  Args:
    type: :Person
    source: Catherine_Princess_of_Wales
  AssignClass (ddb39d4e-b3f5-4c59-aa8b-e87b0780f117)
 Call ID: ddb39d4e-b3f5-4c59-aa8b-e87b0780f117
  Args:
    type: :Woman
    source: Catherine_Princess_of_Wales
  AssignClass (2fe09a9b-3f1e-4dd0-bd2d-b24a8ecd91f1)
 Call ID: 2fe09a9b-3f1e-4dd0-bd2d-b24a8ecd91f1
  Args:
    type: :Person
    source: Charles_III
  AssignClass (ccf165d0-faec-4417-bdd0-3ed9e9de8ac6)
 Call ID: ccf165d0-faec-4417-bdd0-3ed9e9de8ac6
  Args:
    type: :Man
    source: Charles_III
  AssignClass (7d5b4a93-f166-4750-86a1-c4facf963e29)
 Call ID: 7d5b4a93-f166-4750-86a1-c4facf963e29
  Args:
    source: Diana_Princess_of_Wales
    type: :Person
  AssignClass (5adc6126-c1e2-4c90-86d1-f3771d650514)
 Call ID: 5adc6126-c1e2-4c90-86d1-f3771d650514
  Args:
    type: :Woman
    source: Diana_Princess_of_Wales
  AssignClass (74aaaa1d-45a9-4fab-905c-1a4e200bf089)
 Call ID: 74aaaa1d-45a9-4fab-905c-1a4e200bf089
  Args:
    source: George
    type: :Person
  AssignClass (7008bad7-12ce-4715-86cf-0436899335eb)
 Call ID: 7008bad7-12ce-4715-86cf-0436899335eb
  Args:
    type: :Man
    source: George
  AssignClass (c67fed03-609b-4dbe-9d94-bf4c0ff2bcc2)
 Call ID: c67fed03-609b-4dbe-9d94-bf4c0ff2bcc2
  Args:
    type: :Person
    source: Louis
  AssignClass (58a372f7-b479-4ad1-9c4a-140faa8ad537)
 Call ID: 58a372f7-b479-4ad1-9c4a-140faa8ad537
  Args:
    source: Louis
    type: :Man
  AssignClass (5501c176-f984-46d7-9489-b51e74727073)
 Call ID: 5501c176-f984-46d7-9489-b51e74727073
  Args:
    type: :Person
    source: Elizabeth_II
  AssignClass (477faf2e-bf0b-4e78-a0e9-bac049cf0f96)
 Call ID: 477faf2e-bf0b-4e78-a0e9-bac049cf0f96
  Args:
    type: :Woman
    source: Elizabeth_II
  AddTriple (1ed76323-a0c1-45bf-9076-243606922776)
 Call ID: 1ed76323-a0c1-45bf-9076-243606922776
  Args:
    source: Charlotte_of_Wales
    target: William_Prince_of_Wales
    relation: :hasFather
  AddTriple (4a086c93-04ae-4eb9-9b46-db21a10aca24)
 Call ID: 4a086c93-04ae-4eb9-9b46-db21a10aca24
  Args:
    target: Catherine_Princess_of_Wales
    relation: :hasMother
    source: Charlotte_of_Wales
  AddTriple (bbaa2982-783c-4b12-ba74-88052671289b)
 Call ID: bbaa2982-783c-4b12-ba74-88052671289b
  Args:
    target: Charles_III
    relation: :hasParent
    source: Charlotte_of_Wales
  AddTriple (bde7bc06-12ef-426a-a0f9-9e0cfe9fddd8)
 Call ID: bde7bc06-12ef-426a-a0f9-9e0cfe9fddd8
  Args:
    relation: :hasParent
    target: Diana_Princess_of_Wales
    source: Charlotte_of_Wales
  AddTriple (4b29b60f-7b28-47b8-b45a-cfdf38c70c7b)
 Call ID: 4b29b60f-7b28-47b8-b45a-cfdf38c70c7b
  Args:
    relation: :hasBrother
    target: George
    source: Charlotte_of_Wales
  AddTriple (50469a32-673f-4c6d-be2a-ce18bf05024c)
 Call ID: 50469a32-673f-4c6d-be2a-ce18bf05024c
  Args:
    source: Charlotte_of_Wales
    relation: :hasBrother
    target: Louis
  AddLiteral (3ea4c364-62ec-4ca6-8e5d-9888ccf97408)
 Call ID: 3ea4c364-62ec-4ca6-8e5d-9888ccf97408
  Args:
    literal_value: 2015
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Charlotte_of_Wales
  AddTriple (5a0ae8b4-9658-4c0b-b06b-dd95d28e77df)
 Call ID: 5a0ae8b4-9658-4c0b-b06b-dd95d28e77df
  Args:
    target: Charlotte_Elizabeth_Diana
    relation: :knownAs
    source: Charlotte_of_Wales
  AddTriple (aac64a31-4204-4752-9996-b45daa2532c8)
 Call ID: aac64a31-4204-4752-9996-b45daa2532c8
  Args:
    relation: :formerlyKnownAs
    target: Charlotte_Cambridge
    source: Charlotte_of_Wales
  Finish (98d34bfd-3258-48cc-8b17-85f99458f420)
 Call ID: 98d34bfd-3258-48cc-8b17-85f99458f420
  Args:

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Charlotte_of_Wales a :Person,
          :Woman ;
      :formerlyKnownAs data:Charlotte_Cambridge ;
      :hasBirthYear 2015 ;
      :hasBrother data:George,
          data:Louis ;
      :hasFather data:William_Prince_of_Wales ;
      :hasMother data:Catherine_Princess_of_Wales ;
      :hasParent data:Charles_III,
          data:Diana_Princess_of_Wales ;
      :knownAs data:Charlotte_Elizabeth_Diana .

  data:Elizabeth_II a :Person,
          :Woman .

  data:Catherine_Princess_of_Wales a :Person,
          :Woman .

  data:Charles_III a :Man,
          :Person .

  data:Diana_Princess_of_Wales a :Person,
          :Woman .

  data:George a :Man,
          :Person .

  data:Louis a :Man,
          :Person .

  data:William_Prince_of_Wales a :Man,
          :Person .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['Charlotte_Cambridge', 'Charlotte_Elizabeth_Diana']

### Required Correction
According to the pipeline rules, **every node must have a class assigned to it** to ensure the graph is semantically valid. 

Please perform the following steps:
1. Review the input text and ontology to determine the most appropriate class for each node listed above.
2. Use the `AssignClass` tool for each node to assign its correct type.
3. Once all nodes have been assigned a class, you may attempt to `Finish` again or run `ValidateShacl` to verify the final state.

Proceed with the necessary tool calls now.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (634d2f76-4fb3-4800-a53e-1d359b81ebd4)
 Call ID: 634d2f76-4fb3-4800-a53e-1d359b81ebd4
  Args:
    type: :DomainEntity
    source: Charlotte_Elizabeth_Diana
  AssignClass (9d2f957d-1280-4d6e-8103-82842c5215d1)
 Call ID: 9d2f957d-1280-4d6e-8103-82842c5215d1
  Args:
    type: :DomainEntity
    source: Charlotte_Cambridge
  Finish (e46dce04-c2dd-487f-b3f7-c27931355fd2)
 Call ID: e46dce04-c2dd-487f-b3f7-c27931355fd2
  Args: