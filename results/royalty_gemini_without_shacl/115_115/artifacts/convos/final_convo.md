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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Prince Philippos of Greece and Denmark (Greek: Φίλιππος Ντε Γκρες, romanized: Phílippos de Grèce; born 26 April 1986) is the youngest child of Constantine II and Anne-Marie, who were the last King and Queen of Greece, from 1964 to 1973.
Early life and education

Philippos was born at St Mary's Hospital, London, on 26 April 1986, the third son of King Constantine II and Queen Anne-Marie of Greece.
He was baptized in the Greek Orthodox Church at Saint Sophia Cathedral, London, on 10 July 1986, with King Juan Carlos I of Spain, Prince Philip, Duke of Edinburgh, Diana, Princess of Wales, Infanta Elena of Spain, Princess Benedikte of Denmark, Kyril, Prince of Preslav and Penelope, Lady Romsey serving as godparents.
Alongside his four siblings, he is a Director of the Anne-Marie foundation.
Personal life

In 2018, Philippos began dating Nina Nastassja Flohr, the daughter of Swiss businessman Thomas Flohr, who founded the private jet rental company VistaJet, and Katharina Flohr (née Konečný), former Creative Director of Fabergé and editor-in-chief of the Russian Vogue.
That same year, they appeared together in public at the wedding of Princess Eugenie of York and Jack Brooksbank.
They made other appearances as a couple, including the wedding of Lord Edward Spencer-Churchill and Kimberly Hammerstroem in 2018 and the wedding of Jean-Christophe, Prince Napoléon and Countess Olympia von und zu Arco-Zinneberg in 2019.
In 2020 while vacationing in Ithaca, Greece, Flohr and Prince Philippos became engaged.
At this ceremony, Nina wore a wedding dress tailored by Chanel and the diamond Corsage Tiara, which was worn by her sister-in-law, Marie Chantal, at her wedding.
In attendance were Philippos and Nina's parents, siblings, nephews and nieces, as well as extended members of the Greek royal family, such as Queen Sofía of Spain, Prince Michael, Princess Marina and Princess Tatiana Radziwill.
Other attendees included Princess Benedikte of Denmark, the Hereditary Prince and Hereditary Princess of Hanover, Prince and Princess Christian of Hanover, the Prince of Preslav, Princess Beatrice of York, Edoardo Mapelli Mozzi, Princess Eugenie of York, Jack Brooksbank and Sabine Getty, along with her daughter, Gene, who acted as a flower girl.
A reception was held at the National Gymnastics Association and another one at the Piraeus Yacht Club, hosted by Constantine.
On September 28, 2024, Philippos served as a groomsman at the wedding of Princess Theodora of Greece and Denmark and Matthew Kumar at the Metropolitan Cathedral of Athens.
Οn 20 December 2024, Philippos along with the other members of the former royal family acquired Greek citizenship, under the surname De Grece.
The family was deprived of citizenship in 1994 when the former King Constantine refused to acquire a surname, as required by law for all Greek citizens.
Titles, styles and honours

Titles and styles

Following the deposition of the Greek monarchy in 1973, the title "Prince of Greece" with the style of Royal Highness is no longer legally recognised by the government of the Hellenic Republic.
Through his male-line descent from Christian IX of Denmark, he is also a Danish prince with the style of Highness.



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
  AssignClass (fc97ecb1-fe98-4104-a005-0db056c6a475)
 Call ID: fc97ecb1-fe98-4104-a005-0db056c6a475
  Args:
    type: :Man
    source: :Prince_Philippos_of_Greece_and_Denmark
  AssignClass (c230473c-38d8-43e7-bf0f-26cbb7fe0f97)
 Call ID: c230473c-38d8-43e7-bf0f-26cbb7fe0f97
  Args:
    source: :King_Constantine_II
    type: :Man
  AssignClass (fbe877c5-d372-4de8-b809-ddcbce8e4255)
 Call ID: fbe877c5-d372-4de8-b809-ddcbce8e4255
  Args:
    source: :Queen_Anne-Marie
    type: :Woman
  AddLiteral (9dee3040-5ca1-4f6b-968a-a9e1755f03f5)
 Call ID: 9dee3040-5ca1-4f6b-968a-a9e1755f03f5
  Args:
    source: :Prince_Philippos_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 1986
    relation: :hasBirthYear
  AddTriple (13c4e7cb-cce4-4b56-9c87-f8edf53fdc10)
 Call ID: 13c4e7cb-cce4-4b56-9c87-f8edf53fdc10
  Args:
    source: :Prince_Philippos_of_Greece_and_Denmark
    target: :King_Constantine_II
    relation: :hasFather
  AddTriple (05dd00ed-2ebc-46e6-81fc-3b0be804e37e)
 Call ID: 05dd00ed-2ebc-46e6-81fc-3b0be804e37e
  Args:
    source: :Prince_Philippos_of_Greece_and_Denmark
    relation: :hasMother
    target: :Queen_Anne-Marie
  AssignClass (d9c97f53-b525-44d9-a227-01f50e8c2a54)
 Call ID: d9c97f53-b525-44d9-a227-01f50e8c2a54
  Args:
    type: :Woman
    source: :Queen_Sofia_of_Spain
  AssignClass (317cbfdd-17e7-42e2-901c-2134aed2ada2)
 Call ID: 317cbfdd-17e7-42e2-901c-2134aed2ada2
  Args:
    type: :Man
    source: :Prince_Michael
  AssignClass (7f21ff37-9c42-4dd4-9974-3cd3e6437a24)
 Call ID: 7f21ff37-9c42-4dd4-9974-3cd3e6437a24
  Args:
    type: :Woman
    source: :Princess_Marina
  AddTriple (e43a2989-15cd-4f0b-b12d-4937aa25f638)
 Call ID: e43a2989-15cd-4f0b-b12d-4937aa25f638
  Args:
    relation: :hasMarriageYear
    target: :Princess_Marina
    source: :Prince_Michael,target:
  Finish (d12d455a-e861-438d-ba96-9ec5d4d5d118)
 Call ID: d12d455a-e861-438d-ba96-9ec5d4d5d118
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

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Prince_Michael a :Man .

  data:Prince_Michael%2Ctarget :hasMarriageYear data:Princess_Marina .

  data:Prince_Philippos_of_Greece_and_Denmark a :Man ;
      :hasBirthYear 1986 ;
      :hasFather data:King_Constantine_II ;
      :hasMother data:Queen_Anne-Marie .

  data:Queen_Sofia_of_Spain a :Woman .

  data:King_Constantine_II a :Man .

  data:Princess_Marina a :Woman .

  data:Queen_Anne-Marie a :Woman .



================================= Tool Message =================================

### Validation Error: Missing Node Types
Your request to `Finish` has been declined. The following nodes in the Data Graph are missing a class assignment (`rdf:type`):

**Classless Nodes:**
['Prince_Michael%2Ctarget']

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
  RemoveTriple (8935fe36-261d-461e-b33f-fdec318e7042)
 Call ID: 8935fe36-261d-461e-b33f-fdec318e7042
  Args:
    relation: :hasMarriageYear
    target: :Princess_Marina
    source: :Prince_Michael%2Ctarget
  AddTriple (810d0545-a914-4d5f-8065-b0357d393f1f)
 Call ID: 810d0545-a914-4d5f-8065-b0357d393f1f
  Args:
    source: :Prince_Michael
    target: :Princess_Marina
    relation: :hasRelation
  Finish (e64841f0-be94-46f7-a60c-46a4d752d26d)
 Call ID: e64841f0-be94-46f7-a60c-46a4d752d26d
  Args: