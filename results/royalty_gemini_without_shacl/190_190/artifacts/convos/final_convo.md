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
Princess Hélène of Orléans (French: Princesse Hélène Louise Henriette d'Orléans; 13 June 1871 – 21 January 1951) was a member of the deposed Orléans royal family of France and, by marriage to the head of a cadet branch of the Italian royal family, the Duchess of Aosta.
Family

Hélène was the third of eight children born to Prince Philippe, Count of Paris, and Infanta Maria Isabel of Spain.
Her father was a grandson of Louis Philippe I, King of the French, and had been heir-apparent to the throne from 1842 until the exile of the dynasty in 1848.
Repatriating to France at the end of June 1871, the family took up residence in Paris at the Hotel Fould on the Rue du Faubourg Saint-Honoré, as guests of their uncle, Henri, Duke of Aumale, whose wealth and properties in France had not been confiscated in 1852, unlike those of the other Orléans princes.
On 21 December 1872 the National Assembly enacted a law of restitution, authorising restoration of approximately 40 million of the eighty million francs worth of property which had formerly belonged to the House of Orléans, although the actual re-acquisition of that wealth would take several years.
Meanwhile, a close friend of the Count and Countess of Paris, Maria Brignole Sale De Ferrari, placed at their disposal the ground floor and gardens of the Hôtel Matignon on the rue de Varenne in Paris.
Along the adjacent rue de Babylone the Duchess had a two-story town house built to accommodate the Orléans children, their governesses and tutors, which served as Hélène's home from 1876 until her father was again exiled.
In 1883 the last legitimate prince in the male-line of Louis XV, Henri, Count of Chambord, died childless leaving, in the eyes of French royalists excepting recalcitrant legitimists, the Count of Paris as heir to the Bourbon crown of France.
However, celebrations in Paris in the spring of 1886 prior to the marriage in Lisbon of Hélène's eldest sister Amélie to Carlos of Braganza-Coburg, Prince Royal of Portugal, evoked such clear expressions of monarchist support for the House of Orléans that on 22 July the French Republic took the precaution of banishing the heads of France's former ruling dynasties, the Orléans and Bonapartes, from the country.
Nearly all of the Orléans promptly left France, with Hélène and her parents going on to visit Tunbridge Wells in England and then travelling to Scotland before taking up residence in October at Sheen House in East Sheen, England.
Potential matches

Most of Hélène's siblings had married well, including Amélie, Queen of Portugal, Philippe, Duke of Orléans (who married Archduchess Maria Dorothea of Austria) and Isabelle, Duchess of Guise, and Hélène's parents had hopes that she would marry an heir to a throne.
Those hopes were fanned by the fact that Hélène was considered a great beauty for the day, and one contemporary source stated that she was "the personification of womanly health and beauty, distinguished as a graceful athlete and charming linguist".
Relationship with the Duke of Clarence

Prince Albert Victor, Duke of Clarence and Avondale ("Eddy") was the eldest son of the future Edward VII and grandson of then reigning Queen Victoria.
During the spring and summer of 1890, Eddy and Hélène were allowed to become acquainted at the homes of Clarence's sister Princess Louise, Duchess of Fife in Sheen and in Scotland, and, with the encouragement of their mothers, Hélène and Eddy fell in love.
On 29 August, Clarence obtained permission to meet alone with his grandmother at Balmoral Castle in Scotland, and brought Hélène with him.
Marriage to a Catholic would have entailed constitutional forfeiture of Eddy's claim to the British throne, pursuant to the Act of Settlement, but Hélène offered to become an Anglican.
When Queen Victoria expressed surprise at Hélène's offer, Hélène wept and insisted that her willingness to do so was for the sake of love.
This included her expectation that Hélène's father would not consent to his daughter's change of faith.
Hélène's father refused to countenance the marriage, was adamant she could not convert and informed the Queen of his decision.
He granted permission, nonetheless, for Hélène to personally beseech Pope Leo XIII for a dispensation to marry Clarence, but the Pope confirmed her father's verdict and the courtship ended.
Clarence never got over his feelings for Hélène and their relationship is commemorated at his tomb at Windsor Castle by a bead wreath with the single word "HELENE" written upon it.
Queen Victoria wrote to her grandson recommending another of her grandchildren, Princess Margaret of Prussia, as an alternative, but nothing came of that suggestion, and Clarence told his grandmother that his love for another cousin, Alix of Hesse (a match for which the Queen had long hoped) had gone unrequited.
An engagement to Princess Mary of Teck was later arranged, but Clarence died before their wedding could take place.
Although acknowledging his parents' desires for a French alliance in his diary, the future Tsar Nicholas II of Russia (a first cousin of Clarence) never pursued their choice, Hélène, as he was already in love with the aforementioned Alix of Hesse and secured their permission to marry her in 1894.
In 1892, while travelling in Egypt with her brother Philippe, Hélène met Ernst Gunther, Duke of Schleswig-Holstein, who decided that he would marry her, to the fury of his sister, the German Empress Augusta Victoria.
German diplomatic pressure put an end to Ernst Gunther's hopes, which were probably fruitless in any event as Hélène showed no interest in his advances.
In the meantime, he met his future wife, Countess Sophie Chotek, and never considered Hélène again.
Marriage and children

On 25 June 1895, at the Church of St. Raphael in Kingston upon Thames, Hélène married Prince Emanuele Filiberto of Savoy, 2nd Duke of Aosta (1869–1931).
The wedding was attended by Crown Prince Victor Emmanuel of Italy, the Prince and Princess of Wales and others of the British royal family.
The couple had two sons:


Widowed in 1931, Princess Hélène was married for a second time in 1936 to Colonel Otto Campini.
Avocations

In 1892 Hélène travelled with her brother Philippe to Egypt and Palestine, the first of many trips outside of Europe.
After the breakdown of both her health and her marriage, Hélène began frequent trips to Africa which lasted up to ten months at a time.
In 1913-1914 Hélène undertook a round-the-world trip which she recorded in another travel book.
War-time nurse

When the Italo-Turkish War broke out, Hélène trained as a nurse and went aboard the hospital ship Memfi, where she cared for wounded soldiers and those suffering from disease.
During World War I, Hélène became the head of the Italian Red Cross nurses and spent much of her time on or near the front lines.
For her service, Hélène was awarded the Italian Silver Medal for bravery, the Romanian Regina Maria Cross, the French Croix de Guerre, and the Insignia of a Dame Grand Cross of the Order of the British Empire.



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
  AssignClass (a179a609-a840-4d54-bd9b-49952ab8e26e)
 Call ID: a179a609-a840-4d54-bd9b-49952ab8e26e
  Args:
    type: :Woman
    source: Hélène_of_Orléans
  AssignClass (95b0fc9d-92d4-44ff-af27-33ae2e7cab30)
 Call ID: 95b0fc9d-92d4-44ff-af27-33ae2e7cab30
  Args:
    source: Hélène_of_Orléans
    type: :Person
  AddLiteral (0ab56d47-d326-4f5c-b8b2-4cb26da078ef)
 Call ID: 0ab56d47-d326-4f5c-b8b2-4cb26da078ef
  Args:
    literal_type: xsd:integer
    literal_value: 1871
    source: Hélène_of_Orléans
    relation: :hasBirthYear
  AddLiteral (256f4d80-d19f-4410-b238-ebfe8793df84)
 Call ID: 256f4d80-d19f-4410-b238-ebfe8793df84
  Args:
    source: Hélène_of_Orléans
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1951
  AssignClass (679861d7-04e0-4c36-9681-d12ff24e8c27)
 Call ID: 679861d7-04e0-4c36-9681-d12ff24e8c27
  Args:
    source: Prince_Philippe_Count_of_Paris
    type: :Man
  AssignClass (820e2cda-99be-497a-a622-c49bc8bcf8b2)
 Call ID: 820e2cda-99be-497a-a622-c49bc8bcf8b2
  Args:
    source: Prince_Philippe_Count_of_Paris
    type: :Ancestor
  AssignClass (811a3030-ea13-44f9-8ec6-170fe1f30496)
 Call ID: 811a3030-ea13-44f9-8ec6-170fe1f30496
  Args:
    source: Infanta_Maria_Isabel_of_Spain
    type: :Woman
  AssignClass (354badda-8f76-4a17-a9a1-60bee928eed6)
 Call ID: 354badda-8f76-4a17-a9a1-60bee928eed6
  Args:
    type: :Ancestor
    source: Infanta_Maria_Isabel_of_Spain
  AddTriple (a1c2c5d3-4f42-48e5-afe7-7e1cda5885e2)
 Call ID: a1c2c5d3-4f42-48e5-afe7-7e1cda5885e2
  Args:
    target: Prince_Philippe_Count_of_Paris
    source: Hélène_of_Orléans
    relation: :hasFather
  AddTriple (7c9cd432-0a67-4ab0-8efe-d2fb86e13a31)
 Call ID: 7c9cd432-0a67-4ab0-8efe-d2fb86e13a31
  Args:
    target: Infanta_Maria_Isabel_of_Spain
    source: Hélène_of_Orléans
    relation: :hasMother
  AssignClass (8a313cc6-45f2-4820-a487-25af6d69af6a)
 Call ID: 8a313cc6-45f2-4820-a487-25af6d69af6a
  Args:
    type: :Woman
    source: Amélie_of_Orléans
  AddTriple (4a6d10a9-a482-4493-8cda-1bd2d354973f)
 Call ID: 4a6d10a9-a482-4493-8cda-1bd2d354973f
  Args:
    relation: :hasSister
    source: Hélène_of_Orléans
    target: Amélie_of_Orléans
  AssignClass (74117a43-e0d7-4b0a-afd4-71ee4d4a5488)
 Call ID: 74117a43-e0d7-4b0a-afd4-71ee4d4a5488
  Args:
    type: :Man
    source: Philippe_Duke_of_Orléans
  AddTriple (8710a7ab-f19e-4dc2-929b-e25a6a7d3255)
 Call ID: 8710a7ab-f19e-4dc2-929b-e25a6a7d3255
  Args:
    relation: :hasBrother
    source: Hélène_of_Orléans
    target: Philippe_Duke_of_Orléans
  AssignClass (f4fc243e-4926-4c21-a9aa-f7ae5d7f78a6)
 Call ID: f4fc243e-4926-4c21-a9aa-f7ae5d7f78a6
  Args:
    type: :Woman
    source: Isabelle_Duchess_of_Guise
  AddTriple (47399f93-83d2-47f8-a83a-640a8738260e)
 Call ID: 47399f93-83d2-47f8-a83a-640a8738260e
  Args:
    source: Hélène_of_Orléans
    relation: :hasSister
    target: Isabelle_Duchess_of_Guise
  AssignClass (674e05f6-15ae-4db6-ba9a-f4cc77f19b2c)
 Call ID: 674e05f6-15ae-4db6-ba9a-f4cc77f19b2c
  Args:
    source: Prince_Emanuele_Filiberto_of_Savoy
    type: :Man
  AddLiteral (f3960a1c-92ff-4bb1-92be-9122e8be7521)
 Call ID: f3960a1c-92ff-4bb1-92be-9122e8be7521
  Args:
    literal_type: xsd:integer
    literal_value: 1895
    source: Hélène_of_Orléans
    relation: :hasMarriageYear
  AddTriple (5c8c5cec-b9de-417f-a5e4-0023b42bf678)
 Call ID: 5c8c5cec-b9de-417f-a5e4-0023b42bf678
  Args:
    relation: :hasRelation
    source: Hélène_of_Orléans
    target: Prince_Emanuele_Filiberto_of_Savoy
  AssignClass (511b0434-af75-416c-ad76-cd582b0031aa)
 Call ID: 511b0434-af75-416c-ad76-cd582b0031aa
  Args:
    source: Otto_Campini
    type: :Man
  AddLiteral (8f46b458-ff1c-4756-b642-67a2576f50f9)
 Call ID: 8f46b458-ff1c-4756-b642-67a2576f50f9
  Args:
    relation: :hasMarriageYear
    source: Hélène_of_Orléans
    literal_type: xsd:integer
    literal_value: 1936
  AddTriple (b0f3067b-9bbe-4e8e-af2f-209f3b1e7c7e)
 Call ID: b0f3067b-9bbe-4e8e-af2f-209f3b1e7c7e
  Args:
    target: Otto_Campini
    source: Hélène_of_Orléans
    relation: :hasRelation
  Finish (c88a08bc-486a-4348-8d62-1b97aa060b74)
 Call ID: c88a08bc-486a-4348-8d62-1b97aa060b74
  Args: