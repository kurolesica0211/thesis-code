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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Princess Margarita of Bourbon-Parma, Countess of Colorno (Dutch: Margarita Maria Beatrix Prinses de Bourbon de Parme; born 13 October 1972), is the eldest daughter of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
She is a member of the House of Bourbon-Parma as well an extended member of the Dutch royal family.
Per a 1996 royal decree issued by Queen Beatrix, she is entitled to the style and title Her Royal Highness Princess Margarita de Bourbon de Parme in the Netherlands as a member of the extended royal family.
Early life

Born in Nijmegen, she is the twin sister of Prince Jaime.
She also has an elder brother, Prince Carlos, and a younger sister, Princess Carolina.
Her godparents are Queen Beatrix of the Netherlands (maternal aunt) and Prince Sixtus Henry of Bourbon-Parma (paternal uncle).
She is the eldest granddaughter of Queen Juliana and Prince Bernhard.
Together with her mother and her siblings she moved from Spain to The Netherlands, to live with her grandparents, Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld at Baarn.
Margarita studied Cultural Anthropology at the Vrije Universiteit of Amsterdam and is an interior decorator.
First marriage and controversy

On 19 June 2001, Princess Margarita married the entrepreneur Edwin Karel Willem de Roy van Zuydewijn, member of a Dutch patrician family.
In 2003, a series of incidents became known as the Margarita-affair.
Margarita and her husband accused the Dutch Royal House and the Dutch secret service of obstructing the affairs of Fincentives, the company of de Roy van Zuydewijn.
The couple's home was the Bartas Castle in Saint-Georges, Gers, France, but by 2004 the princess was increasingly seen more often in Amsterdam than there.
Because of the quarrels between the princess and the Dutch Royal family during the Margarita-affair, she was not welcome at the marriage of her cousin Willem-Alexander, Prince of Orange to Máxima Zorreguieta, or at the funeral of her uncle, Prince Claus of the Netherlands.
On 20 February 2023, Princess Margarita and Ten Cate announced their divorce.
Together they have two daughters:


Margarita currently lives in Wassenaar.
Titles, styles and honours

Already a ducal princess from birth, her father bestowed on 2 September 1996 the substantive title Contessa di Colorno (Countess of Colorno) upon her.
The same year she was incorporated into the Dutch nobility by her aunt Queen Beatrix, with the highest noble title Prinses de Bourbon de Parme (Princess of Bourbon-Parma) and styled Hare Koninklijke Hoogheid (Her Royal Highness).
She does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a granddaughter of Queen Juliana, she is officially a member of the more extended Dutch royal family.
Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (09a917f0-f1bb-4efb-ad96-9fd73a5ae52b)
 Call ID: 09a917f0-f1bb-4efb-ad96-9fd73a5ae52b
  Args:
    type: :Woman
    source: Princess_Margarita_of_Bourbon_Parma
  AssignClass (cd28100e-1c7e-470f-aba0-0d1561f79b7d)
 Call ID: cd28100e-1c7e-470f-aba0-0d1561f79b7d
  Args:
    source: Princess_Irene_of_the_Netherlands
    type: :Woman
  AssignClass (956cba0c-13d8-42be-b405-ac5cead024ba)
 Call ID: 956cba0c-13d8-42be-b405-ac5cead024ba
  Args:
    type: :Man
    source: Carlos_Hugo_Duke_of_Parma
  AssignClass (6e22b4a2-0105-45f1-a744-042f215ad3d1)
 Call ID: 6e22b4a2-0105-45f1-a744-042f215ad3d1
  Args:
    source: Prince_Jaime
    type: :Man
  AssignClass (f04ac455-83c5-45ca-9e26-6b29772ae1f5)
 Call ID: f04ac455-83c5-45ca-9e26-6b29772ae1f5
  Args:
    type: :Man
    source: Prince_Carlos
  AssignClass (fd1749a4-82e2-42ba-999c-d5565602c2ed)
 Call ID: fd1749a4-82e2-42ba-999c-d5565602c2ed
  Args:
    source: Princess_Carolina
    type: :Woman
  AssignClass (836e7da9-a2e3-4d5d-b8de-2fd802940076)
 Call ID: 836e7da9-a2e3-4d5d-b8de-2fd802940076
  Args:
    source: Queen_Juliana
    type: :Woman
  AssignClass (fe250d46-b730-4329-bdcc-17362c43a8ce)
 Call ID: fe250d46-b730-4329-bdcc-17362c43a8ce
  Args:
    source: Prince_Bernhard
    type: :Man
  AssignClass (f64917f4-cbd4-4f0b-bff3-d1238d654f0a)
 Call ID: f64917f4-cbd4-4f0b-bff3-d1238d654f0a
  Args:
    source: Edwin_Karel_Willem_de_Roy_van_Zuydewijn
    type: :Man
  AddTriple (4c7dfaca-0eb1-474d-a17a-eea7f154f44d)
 Call ID: 4c7dfaca-0eb1-474d-a17a-eea7f154f44d
  Args:
    source: Princess_Margarita_of_Bourbon_Parma
    target: Princess_Irene_of_the_Netherlands
    relation: :hasMother
  AddTriple (98c36e75-1535-47fa-b59b-134b0b4fe3f4)
 Call ID: 98c36e75-1535-47fa-b59b-134b0b4fe3f4
  Args:
    relation: :hasFather
    target: Carlos_Hugo_Duke_of_Parma
    source: Princess_Margarita_of_Bourbon_Parma
  AddLiteral (9d5c3207-3e3d-4b1a-9fb5-46997e1b06f0)
 Call ID: 9d5c3207-3e3d-4b1a-9fb5-46997e1b06f0
  Args:
    relation: :hasBirthYear
    literal_value: 1972
    literal_type: xsd:integer
    source: Princess_Margarita_of_Bourbon_Parma
  AddTriple (1b79c64e-19f4-44e4-af92-7a89bcc2ce51)
 Call ID: 1b79c64e-19f4-44e4-af92-7a89bcc2ce51
  Args:
    relation: :isSiblingOf
    target: Prince_Jaime
    source: Princess_Margarita_of_Bourbon_Parma
  AddTriple (2b8eb216-0bb2-41a4-8bc1-ebb06f3c6b7a)
 Call ID: 2b8eb216-0bb2-41a4-8bc1-ebb06f3c6b7a
  Args:
    relation: :isSiblingOf
    target: Prince_Carlos
    source: Princess_Margarita_of_Bourbon_Parma
  AddTriple (92538b64-d042-4d66-b042-a8ca0b06970d)
 Call ID: 92538b64-d042-4d66-b042-a8ca0b06970d
  Args:
    target: Princess_Carolina
    source: Princess_Margarita_of_Bourbon_Parma
    relation: :isSiblingOf
  AddTriple (f3e37151-1801-417d-b273-6d6019ad8d5f)
 Call ID: f3e37151-1801-417d-b273-6d6019ad8d5f
  Args:
    target: Princess_Irene_of_the_Netherlands
    source: Prince_Bernhard
    relation: :isFatherOf
  AddTriple (1c73ad41-396c-4e09-8255-b27963522405)
 Call ID: 1c73ad41-396c-4e09-8255-b27963522405
  Args:
    target: Princess_Irene_of_the_Netherlands
    source: Queen_Juliana
    relation: :isMotherOf
  AddLiteral (65db03bc-30b1-48e2-b2f4-7c4f44a7b675)
 Call ID: 65db03bc-30b1-48e2-b2f4-7c4f44a7b675
  Args:
    relation: :hasMarriageYear
    literal_value: 2001
    literal_type: xsd:integer
    source: Princess_Margarita_of_Bourbon_Parma
  Finish (2ee75f72-9dd4-43f9-9b20-f5a1f152a18b)
 Call ID: 2ee75f72-9dd4-43f9-9b20-f5a1f152a18b
  Args: