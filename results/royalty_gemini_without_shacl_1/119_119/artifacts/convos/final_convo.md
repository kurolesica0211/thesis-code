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
Grand Duke HenriGrand Duchess Maria Teresa


Princess Joan


Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Prince Guillaume of Luxembourg (Guillaume Marie Louis Christian; born 1 May 1963) is the third son and youngest child of Grand Duke Jean and Grand Duchess Josephine-Charlotte of Luxembourg.
On the night of 10 to 11 September 2000, Prince Guillaume and Princess Sibilla were involved in a serious car accident near Paris.
Marriage and children

Prince Guillaume married Sibilla Sandra Weiller y Torlonia (b. 12 June 1968, Neuilly-sur-Seine, France), the second child of French industrialist and patron of the Arts Paul-Annik Weiller (son of Paul-Louis Weiller and Aliki, Lady Russell) and Italian noblewoman Donna Olimpia Torlonia di Civitella-Cesi (daughter of Alessandro Torlonia, 5th Prince of Civitella-Cesi and Infanta Beatriz of Spain) and the second cousin of King Felipe VI of Spain civilly in Sélestat on 8 September 1994 and religiously at Versailles Cathedral on 24 September 1994, who received the title "Princess of Luxembourg".
Guillaume and Sibilla have four children:


Their sons are in the line of succession to the throne of Luxembourg.
Prince Guillaume is godfather to his nephew, Guillaume V, Grand Duke of Luxembourg.
He is also one of the godparents of Prince Achileas-Andreas of Greece and Denmark, the second son of Pavlos, Crown Prince of Greece.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (8e3a1c47-eb94-4ca5-8875-07771598cc5b)
 Call ID: 8e3a1c47-eb94-4ca5-8875-07771598cc5b
  Args:
    type: :Man
    source: GrandDukeHenri
  AssignClass (eb65bfa4-2dac-44f3-b740-66e6a4b77071)
 Call ID: eb65bfa4-2dac-44f3-b740-66e6a4b77071
  Args:
    type: :Woman
    source: GrandDuchessMariaTeresa
  AssignClass (d96fec23-7223-440d-bf5f-495c73db66cf)
 Call ID: d96fec23-7223-440d-bf5f-495c73db66cf
  Args:
    type: :Woman
    source: PrincessJoan
  AssignClass (5b1afc7c-2526-4010-bf92-bd356feb376e)
 Call ID: 5b1afc7c-2526-4010-bf92-bd356feb376e
  Args:
    type: :Man
    source: PrinceFelix
  AssignClass (eb637b62-264f-4b28-ba3f-6a6ea99024e0)
 Call ID: eb637b62-264f-4b28-ba3f-6a6ea99024e0
  Args:
    type: :Man
    source: PrinceRene
  AssignClass (8d7522d0-70d7-4033-b6f6-9e870809c00e)
 Call ID: 8d7522d0-70d7-4033-b6f6-9e870809c00e
  Args:
    type: :Woman
    source: PrincessMariaPia
  AssignClass (c07d75f3-df3c-4a96-bb81-c22f910d2b75)
 Call ID: c07d75f3-df3c-4a96-bb81-c22f910d2b75
  Args:
    type: :Woman
    source: PrincessMarina
  AssignClass (da9de79e-a1a7-4e83-a709-66fdd4061b17)
 Call ID: da9de79e-a1a7-4e83-a709-66fdd4061b17
  Args:
    type: :Man
    source: PrinceLouis
  AssignClass (df498f2f-631b-4102-99cb-8d85a758d5bf)
 Call ID: df498f2f-631b-4102-99cb-8d85a758d5bf
  Args:
    type: :Man
    source: PrinceRemy
  AssignClass (782d3d94-355d-4d28-8501-c430e7f37cdc)
 Call ID: 782d3d94-355d-4d28-8501-c430e7f37cdc
  Args:
    type: :Woman
    source: PrincessElisabeth
  AssignClass (ddc3ef26-a235-4f95-a725-de37f6ae6311)
 Call ID: ddc3ef26-a235-4f95-a725-de37f6ae6311
  Args:
    type: :Woman
    source: PrincessChantal
  AssignClass (5009c083-2d63-493e-9a19-ec6079d1343c)
 Call ID: 5009c083-2d63-493e-9a19-ec6079d1343c
  Args:
    type: :Man
    source: PrinceJean
  AssignClass (f9bccd02-dafb-4f0f-888b-955fe3a2eb7e)
 Call ID: f9bccd02-dafb-4f0f-888b-955fe3a2eb7e
  Args:
    type: :Woman
    source: PrincessVirginia
  AssignClass (29132d94-e72c-4f5f-a28b-00ce86b3bc67)
 Call ID: 29132d94-e72c-4f5f-a28b-00ce86b3bc67
  Args:
    type: :Man
    source: PrinceGuillaumeOfLuxembourg
  AssignClass (6e174d4c-ec45-4c3c-a72d-6a57804cb17d)
 Call ID: 6e174d4c-ec45-4c3c-a72d-6a57804cb17d
  Args:
    type: :Man
    source: GrandDukeJean
  AssignClass (3a1348e7-e56e-40b0-80c8-7fc0033583a0)
 Call ID: 3a1348e7-e56e-40b0-80c8-7fc0033583a0
  Args:
    type: :Woman
    source: GrandDuchessJosephineCharlotte
  AssignClass (2976f1cc-6b93-471e-8912-67898f047418)
 Call ID: 2976f1cc-6b93-471e-8912-67898f047418
  Args:
    type: :Woman
    source: PrincessSibilla
  AssignClass (f591047f-aa0e-4061-aac5-8e685a35fa95)
 Call ID: f591047f-aa0e-4061-aac5-8e685a35fa95
  Args:
    type: :Man
    source: PaulAnnikWeiller
  AssignClass (5c96d370-131b-48c9-ab06-df1d4955720c)
 Call ID: 5c96d370-131b-48c9-ab06-df1d4955720c
  Args:
    type: :Woman
    source: DonnaOlimpiaTorlonia
  AssignClass (edb23389-aa99-40cd-8268-0f32e1c4a1af)
 Call ID: edb23389-aa99-40cd-8268-0f32e1c4a1af
  Args:
    type: :Man
    source: PaulLouisWeiller
  AssignClass (cdba0f59-7a99-4339-957f-b9495f222a01)
 Call ID: cdba0f59-7a99-4339-957f-b9495f222a01
  Args:
    type: :Woman
    source: AlikiLadyRussell
  AssignClass (a81a447b-7b71-47d7-95d2-d245a83eaf5b)
 Call ID: a81a447b-7b71-47d7-95d2-d245a83eaf5b
  Args:
    type: :Man
    source: AlessandroTorlonia
  AssignClass (75394026-0c1b-4f69-ba55-e50a7fd0c87c)
 Call ID: 75394026-0c1b-4f69-ba55-e50a7fd0c87c
  Args:
    type: :Woman
    source: InfantaBeatriz
  AddTriple (96c9cedf-4ffb-4a4d-85b6-74356accef59)
 Call ID: 96c9cedf-4ffb-4a4d-85b6-74356accef59
  Args:
    relation: :hasFather
    source: PrinceGuillaumeOfLuxembourg
    target: GrandDukeJean
  AddTriple (33b8a99a-d290-4b38-9e27-6e9cb99dff20)
 Call ID: 33b8a99a-d290-4b38-9e27-6e9cb99dff20
  Args:
    target: GrandDuchessJosephineCharlotte
    relation: :hasMother
    source: PrinceGuillaumeOfLuxembourg
  AddLiteral (e4253045-5049-4402-9413-a77650dc2876)
 Call ID: e4253045-5049-4402-9413-a77650dc2876
  Args:
    literal_type: xsd:integer
    source: PrinceGuillaumeOfLuxembourg
    literal_value: 1963
    relation: :hasBirthYear
  AddTriple (d71a0cc7-f475-4e1d-a10b-134c2f9bb88f)
 Call ID: d71a0cc7-f475-4e1d-a10b-134c2f9bb88f
  Args:
    target: PaulAnnikWeiller
    relation: :hasFather
    source: PrincessSibilla
  AddTriple (2d5edd12-f6f2-4aaf-9228-ce493fc3ef99)
 Call ID: 2d5edd12-f6f2-4aaf-9228-ce493fc3ef99
  Args:
    target: DonnaOlimpiaTorlonia
    relation: :hasMother
    source: PrincessSibilla
  AddLiteral (1d28472e-51b2-497c-aa50-f232f8f0f51f)
 Call ID: 1d28472e-51b2-497c-aa50-f232f8f0f51f
  Args:
    relation: :hasBirthYear
    literal_value: 1968
    source: PrincessSibilla
    literal_type: xsd:integer
  AddTriple (b2c7df7c-a5a4-4242-a383-f1d18030e68b)
 Call ID: b2c7df7c-a5a4-4242-a383-f1d18030e68b
  Args:
    target: PaulLouisWeiller
    source: PaulAnnikWeiller
    relation: :hasFather
  AddTriple (f0cd4abb-07fd-4c6e-a158-27b67b80bb18)
 Call ID: f0cd4abb-07fd-4c6e-a158-27b67b80bb18
  Args:
    target: AlikiLadyRussell
    source: PaulAnnikWeiller
    relation: :hasMother
  AddTriple (8b7b9923-ee80-4438-9a32-a21560d8c1e6)
 Call ID: 8b7b9923-ee80-4438-9a32-a21560d8c1e6
  Args:
    target: AlessandroTorlonia
    source: DonnaOlimpiaTorlonia
    relation: :hasFather
  AddTriple (f4ab9b06-e6b7-4636-8c17-f5447e909a1e)
 Call ID: f4ab9b06-e6b7-4636-8c17-f5447e909a1e
  Args:
    target: InfantaBeatriz
    source: DonnaOlimpiaTorlonia
    relation: :hasMother
  AddLiteral (451628b4-1aa4-4151-832c-9a277a422297)
 Call ID: 451628b4-1aa4-4151-832c-9a277a422297
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: PrinceGuillaumeOfLuxembourg
    literal_value: 1994
  AddTriple (5edbb65b-1022-4fc6-b98e-bb94a891b91f)
 Call ID: 5edbb65b-1022-4fc6-b98e-bb94a891b91f
  Args:
    relation: :hasRelation
    source: PrinceGuillaumeOfLuxembourg
    target: PrincessSibilla
  Finish (804a7629-87b3-4f28-9e47-1c52e16a7fa1)
 Call ID: 804a7629-87b3-4f28-9e47-1c52e16a7fa1
  Args: